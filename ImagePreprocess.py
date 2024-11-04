import torch
from PIL import Image
from torchvision.transforms import ToTensor

def preprocess_image(image_path):
    """
    Preprocess the input image for the model.

    Parameters:
    - image_path (str): Path to the image file.

    Returns:
    - torch.Tensor: Preprocessed image tensor ready for the model.
    """
    img = Image.open(image_path)
    img = img.convert('L').resize((28, 28))
    img_tensor = ToTensor()(img).unsqueeze(0)  # Shape: (1, 1, 28, 28)

    return img_tensor

if __name__ == "__main__":

    image_path = ''
    processed_tensor = preprocess_image(image_path)
    print(f'Processed image tensor shape: {processed_tensor.shape}')