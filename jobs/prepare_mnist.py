#!/usr/bin/env python3
"""Data preparation pipeline for MNIST dataset"""
import torch
import torchvision
import torchvision.transforms as transforms
from pathlib import Path

def prepare_data():
    """Download and preprocess MNIST dataset"""
    print("[Data Prep] Starting MNIST data preparation...")
    
    # Create data directory
    data_dir = Path('./data')
    data_dir.mkdir(exist_ok=True)
    
    # Define transforms
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))  # MNIST mean/std
    ])
    
    # Download training data
    print("[Data Prep] Downloading training data...")
    train_dataset = torchvision.datasets.MNIST(
        root='/root/data', 
        train=True, 
        download=True, 
        transform=transform
    )
    
    # Download test data
    print("[Data Prep] Downloading test data...")
    test_dataset = torchvision.datasets.MNIST(
        root='/root/data', 
        train=False, 
        download=True, 
        transform=transform
    )
    
    # Data statistics
    print(f"[Data Prep] Training samples: {len(train_dataset)}")
    print(f"[Data Prep] Test samples: {len(test_dataset)}")
    print(f"[Data Prep] Classes: {train_dataset.classes}")
    
    # Validate data quality
    sample, label = train_dataset[0]
    print(f"[Data Prep] Sample shape: {sample.shape}")
    print(f"[Data Prep] Label range: 0-{len(train_dataset.classes)-1}")
    
    print("[Data Prep] ✓ Data preparation complete")
    return train_dataset, test_dataset

if __name__ == "__main__":
    prepare_data()
