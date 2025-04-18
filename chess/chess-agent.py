import torch
import torch.nn as nn
import torch.optim as optim

import gymnasium
import numpy as np
import openai
import chess

class ChessNet(nn.Module):
    def __init__(self):
        super(ChessNet, self).__init__()
        self.conv1 = nn.Conv2d(14, 64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        self.res_blocks = nn.Sequential(*[ResBlock(64) for _ in range(20)])
        self.policy_head = nn.Conv2d(64, 73, kernel_size=1)  # 73 squares, each can be a move source
        self.value_head = nn.Sequential(
            nn.Conv2d(64, 1, kernel_size=1),
            nn.BatchNorm2d(1),
            nn.Flatten(),
            nn.Linear(8 * 8, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
            nn.Tanh()
        )

    def forward(self, x):
        x = torch.relu(self.bn1(self.conv1(x)))
        x = self.res_blocks(x)
        policy = self.policy_head(x)
        value = self.value_head(x)
        return torch.flatten(policy, 1), value


class ResBlock(nn.Module):
    def __init__(self, channels):
        super(ResBlock, self).__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x):
        residual = x
        x = torch.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        x += residual
        return torch.relu(x)


# Example usage
model = ChessNet()
optimizer = optim.Adam(model.parameters(), lr=0.001)
input_tensor = torch.randn(1, 14, 8, 8)  # Example tensor representing a chess board
policy, value = model(input_tensor)

# Define your loss functions and add training loop here
