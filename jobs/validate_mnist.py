#!/usr/bin/env python3
"""Model validation script for trained MNIST model"""
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from pathlib import Path

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

def validate_model(model_path='/root/models/mnist_final.pth'):
    """Validate trained model on test set"""
    print("[Validation] Loading test data...")
    
    transform = transforms.Compose([transforms.ToTensor()])
    test_dataset = torchvision.datasets.MNIST(
        root='/root/data', 
        train=False, 
        download=True, 
        transform=transform
    )
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64)
    
    # Load model
    model = Net()
    if Path(model_path).exists():
        model.load_state_dict(torch.load(model_path, weights_only=True))
        print(f"[Validation] Loaded model from {model_path}")
    else:
        print(f"[Validation] No checkpoint found at {model_path}, using untrained model")
    
    model.eval()
    
    # Evaluate
    correct = 0
    total = 0
    total_loss = 0
    criterion = nn.CrossEntropyLoss()
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    accuracy = 100 * correct / total
    avg_loss = total_loss / len(test_loader)
    
    print(f"[Validation] ✓ Accuracy: {accuracy:.2f}%")
    print(f"[Validation] ✓ Average Loss: {avg_loss:.4f}")
    print(f"[Validation] ✓ Correct: {correct}/{total}")
    
    return accuracy, avg_loss

if __name__ == "__main__":
    validate_model()
