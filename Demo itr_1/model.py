import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Data preperation
transform = transforms.Compose([
    transforms.ToTensor(),
    # transforms.Resize((28,28)) By default the images are 28x28
])

training_data = datasets.MNIST(root ='./data', train = True, transform=transform, download=True)
test_data = datasets.MNIST(root='./data',train=False, transform=transform)

# Hyperparameters
batch_size = 64  # samples per batch
learning_rate = 0.001  # Initial learning rate
epochs = 10  # iteration

train_dataloader = DataLoader(dataset=training_data, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(dataset=test_data, batch_size=batch_size, shuffle=False)

class NN(torch.nn.Module):
  def __init__(self):
    super(NN, self).__init__()

    # Input layer to first hidden layer
    self.layer1 = nn.Linear(28*28, 128)

    # 2 Hidden layer
    self.layer2 = nn.Linear(128, 64)
    self.layer3 = nn.Linear(64, 32)

    # Output layer (has 10 neurons)
    self.layer4 = nn.Linear(32, 10)

  def forward(self,x):
    x = x.view(-1, 784)  # flatten input data

    # ReLu activation function for hidden layer
    x = torch.relu(self.layer1(x))
    x = torch.relu(self.layer2(x))
    x = torch.relu(self.layer3(x))
    x = self.layer4(x)

    return x

model = NN()

criteria = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(epochs):
    total_loss = 0.0

    for batch_index, (inputs, labels) in enumerate(train_dataloader):
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criteria(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    average_loss = total_loss/len(train_dataloader)
    print('Epoch',epoch + 1,'Average Loss =',average_loss)

print('Training over')

model.eval()

total_test_loss = 0
correct_predictions = 0

with torch.no_grad():
    for batch_data, batch_labels in test_dataloader:
        outputs = model(batch_data)
        loss = criteria(outputs, batch_labels)
        total_test_loss += loss.item()
        _, predicted_classes = torch.max(outputs, 1)
        correct_predictions += (predicted_classes == batch_labels).sum().item()

accuracy = correct_predictions / len(test_data)
average_test_loss = total_test_loss / len(test_dataloader)
print('Test Loss:', average_test_loss, 'Accuracy:', accuracy * 100, '%')

torch.save(model.state_dict(), 'model.pth')
print('model saved')