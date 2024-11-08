import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Define the same SimpleNN model from before
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(28*28, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.flatten(x)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Load the trained model
model = SimpleNN()
model.load_state_dict(torch.load('pytorch_mnist.pth'))
model.eval()


## Uncomment this and run this once , this creates a pytorch_mnist.pth file 
# when done comment again from here

# # Transform for testing
# transform = transforms.Compose([
#     transforms.ToTensor(),
#     transforms.Normalize((0.5,), (0.5,))
# ])

# # Load the test data
# test_data = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
# test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

# # Define the loss function
# criterion = nn.CrossEntropyLoss()

# # Evaluate the model
# correct = 0
# total = 0
# test_loss = 0.0

# with torch.no_grad():
#     for images, labels in test_loader:
#         outputs = model(images)
#         loss = criterion(outputs, labels)
#         test_loss += loss.item()

#         # Get predicted labels
#         _, predicted = torch.max(outputs, 1)
#         total += labels.size(0)
#         correct += (predicted == labels).sum().item()

# accuracy = 100 * correct / total
# average_loss = test_loss / len(test_loader)

# print(f"Loss: {average_loss:.2f}")
# print(f"Accuracy: {accuracy:.2f}%")

# to here, 

#model is trained but the reshape needs to be taken care off , 
# +28x28 is the limit i think neither should we use extra colors cz model does not support them



# prediction from here
from PIL import Image
def predict_image(image_path):
    image = Image.open(image_path).convert('L')
    image = image.resize((28, 28))
    
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    image_tensor = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(image_tensor)
        _, predicted_label = torch.max(output, 1)
    
    return predicted_label.item()

image_path = '3.png'
predicted_digit = predict_image(image_path)
print(f"Predicted digit: {predicted_digit}")