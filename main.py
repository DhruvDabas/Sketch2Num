# from torch import nn, save, load
# from torch import optim
# from torchvision import datasets
# from torch.utils.data import DataLoader
# from torchvision.transforms import ToTensor
# import torch

# train = datasets.MNIST(root="data", download=True, train=True, transform=ToTensor())
# train_loader = DataLoader(train, batch_size=32, shuffle=True)

# class ImageClassifier(nn.Module):
#     def __init__(self) -> None:
#         super().__init__()
#         self.model = nn.Sequential(
#             nn.Conv2d(1, 32, (3, 3)),
#             nn.ReLU(),
#             nn.Conv2d(32, 64, (3, 3)),
#             nn.ReLU(),
#             nn.Conv2d(64, 64, (3, 3)),
#             nn.ReLU(),
#             nn.Flatten(),
#             nn.Linear(64 * (28 - 6) * (28 - 6), 10)  
#         )

#     def forward(self, x):
#         return self.model(x)
    
# clf = ImageClassifier().to('cpu')
# opt = optim.Adam(clf.parameters(), lr=1e-3)
# loss_fn = nn.CrossEntropyLoss()

# if __name__ == "__main__":

#     for epoch in range(10):
#         for batch in train_loader:
#             X, y = batch
#             X, y = X.to('cpu'), y.to('cpu')
#             yhat = clf(X)
#             loss = loss_fn(yhat, y)

#             opt.zero_grad()
#             loss.backward()
#             opt.step()

#         print(f"Epoch {epoch} loss is {loss.item()}")

#     with open ('model_state.pt', 'wb') as f:
#         save(clf.state_dict(),f)
    

from torch import nn, save, load
from torch import optim
from torchvision import datasets
from torch.utils.data import DataLoader
from torchvision.transforms import ToTensor
import torch
from PIL import Image

train = datasets.MNIST(root="data", download=True, train=True, transform=ToTensor())
train_loader = DataLoader(train, batch_size=32, shuffle=True)

class ImageClassifier(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(1, 32, (3, 3)),
            nn.ReLU(),
            nn.Conv2d(32, 64, (3, 3)),
            nn.ReLU(),
            nn.Conv2d(64, 64, (3, 3)),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(64 * (28 - 6) * (28 - 6), 10)  
        )

    def forward(self, x):
        return self.model(x)
    
clf = ImageClassifier().to('cpu')
opt = optim.Adam(clf.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()

if __name__ == "__main__":
    with open('model_state.pt','rb') as f:
        clf.load_state_dict(load(f))
    
    img = Image.open('img_3.jpg')
    img_tensor = ToTensor()(img).unsqueeze(0).to('cpu')

    print(torch.argmax(clf(img_tensor)))

    # for epoch in range(10):
    #     for batch in train_loader:
    #         X, y = batch
    #         X, y = X.to('cpu'), y.to('cpu')
    #         yhat = clf(X)
    #         loss = loss_fn(yhat, y)

    #         opt.zero_grad()
    #         loss.backward()
    #         opt.step()

    #     print(f"Epoch {epoch} loss is {loss.item()}")

    # with open ('model_state.pt', 'wb') as f:
    #     save(clf.state_dict(),f)