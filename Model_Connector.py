import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps

model = tf.keras.models.load_model('mnist_model.h5')

def preprocess(image):
    #convert to greyscale
    image = image.convert('L')
    image_np = np.array(image)

    #threshold to make it binary
    image_np = np.where(image_np > 128, 255, 0).astype(np.uint8)

    #bounding box of non-zero pixels
    coords = np.column_stack(np.where(image_np > 0))
    if coords.shape[0] == 0:
        #if empty image
        return np.zeros((28, 28), dtype=np.float32)

    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0)
    cropped = image_np[y0:y1 + 1, x0:x1 + 1]

    # resize cropped digit keeping aspect ratio of the image
    h, w = cropped.shape
    scale = 20.0 / max(h, w)
    new_h = int(h * scale)
    new_w = int(w * scale)
    digit = Image.fromarray(cropped).resize((new_w, new_h), Image.Resampling.LANCZOS)

    # centered
    canvas = Image.new('L', (28, 28), 0)
    upper_left = ((28 - new_w) // 2, (28 - new_h) // 2)
    canvas.paste(digit, upper_left)

    arr = np.array(canvas).astype(np.float32) / 255.0
    return arr

def PredictImage(image_path):
    image = Image.open(image_path)
    processed = preprocess(image)
    image_tensor = processed.reshape(1, 28, 28, 1)

    prediction = model.predict(image_tensor, verbose=0)
    predicted_label = np.argmax(prediction)

    return predicted_label