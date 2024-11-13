import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

# Define the same SimpleNN model from before
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(28 * 28, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 10)
    
    def forward(self, x):
        x = self.flatten(x)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = self.fc4(x)
        return x


model = SimpleNN()
model.load_state_dict(torch.load('Mnist_Model.pth', weights_only=True))
model.eval()

# prediction from here
def PredictImage(image_path):
    image = Image.open(image_path).convert('L')
    
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    image_tensor = transform(image).unsqueeze(0)  # Add batch dimension (1, 1, 28, 28)
    
    with torch.no_grad():
        output = model(image_tensor)
        _, predicted_label = torch.max(output, 1)
    
    return predicted_label.item()