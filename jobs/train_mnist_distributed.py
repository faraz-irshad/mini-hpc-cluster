import os
import socket
import torch
import torch.nn as nn
import torch.optim as optim
import torch.distributed as dist
import torchvision
import torchvision.transforms as transforms
from torch.nn.parallel import DistributedDataParallel as DDP

# --- Setup distributed environment ---
def setup():
    # Get info from environment variables
    rank = int(os.environ["RANK"])
    world_size = int(os.environ["WORLD_SIZE"])
    master_addr = os.environ["MASTER_ADDR"]
    master_port = os.environ["MASTER_PORT"]

    dist.init_process_group(
        backend="gloo", 
        init_method=f"tcp://{master_addr}:{master_port}",
        rank=rank,
        world_size=world_size,
    )
    print(f"[INFO] Process {rank}/{world_size} initialized on {socket.gethostname()}")

def cleanup():
    dist.destroy_process_group()

# --- Model ---
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(28*28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 28*28)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def main():
    setup()

    # Distributed parameters
    rank = int(os.environ["RANK"])
    world_size = int(os.environ["WORLD_SIZE"])
    device = torch.device("cpu")

    # Data
    transform = transforms.Compose([transforms.ToTensor()])
    dataset = torchvision.datasets.MNIST(root='/root/data', train=True, download=True, transform=transform)

    # Each worker gets data
    train_sampler = torch.utils.data.distributed.DistributedSampler(
        dataset,
        num_replicas=world_size,
        rank=rank,
        shuffle=True
    )
    trainloader = torch.utils.data.DataLoader(dataset, batch_size=64, sampler=train_sampler)

    model = Net().to(device)
    ddp_model = DDP(model)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(ddp_model.parameters(), lr=0.01)

    for epoch in range(20):
        for batch, (inputs, labels) in enumerate(trainloader):
            optimizer.zero_grad()
            outputs = ddp_model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            if batch % 200 == 0:
                print(f"[Rank {rank}] Epoch {epoch} Batch {batch} Loss {loss.item():.4f}")
        
        # Save checkpoint every 5 epochs (only on master)
        if rank == 0 and epoch % 5 == 0:
            checkpoint_path = f"/root/models/mnist_epoch_{epoch}.pth"
            torch.save(model.state_dict(), checkpoint_path)
            print(f"[Rank {rank}] Saved checkpoint: {checkpoint_path}")

    # Save final model (only on master)
    if rank == 0:
        torch.save(model.state_dict(), "/root/models/mnist_final.pth")
        print(f"[Rank {rank}] Saved final model: /root/models/mnist_final.pth")

    cleanup()
    print(f"[Rank {rank}] Training finished.")

if __name__ == "__main__":
    main()
