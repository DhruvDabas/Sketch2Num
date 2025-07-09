import tensorflow as tf
from functools import partial

(mnist_images, mnist_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

mnist_images = mnist_images/255.0
test_images = test_images/255.0

# Data augmentation
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
   rotation_range=10,
   zoom_range=0.1,
   width_shift_range=0.1,
   height_shift_range=0.1,
   shear_range=0.1,
   fill_mode='nearest'
)

DefaultConv2D = partial(tf.keras.layers.Conv2D, kernel_size=3, padding='same', activation='relu', kernel_initializer="he_normal")

model = tf.keras.Sequential([
   DefaultConv2D(filters=32, kernel_size=3, input_shape=[28,28,1]),
   DefaultConv2D(filters=32),
   tf.keras.layers.MaxPool2D(),
   tf.keras.layers.Dropout(0.25),
   
   DefaultConv2D(filters=64),
   DefaultConv2D(filters=64),
   tf.keras.layers.MaxPool2D(),
   tf.keras.layers.Dropout(0.25),
   
   DefaultConv2D(filters=128),
   DefaultConv2D(filters=128),
   DefaultConv2D(filters=128),
   tf.keras.layers.MaxPool2D(),
   tf.keras.layers.Dropout(0.25),
   
   DefaultConv2D(filters=256),
   DefaultConv2D(filters=256),
   tf.keras.layers.GlobalAveragePooling2D(),
   tf.keras.layers.Dropout(0.5),

   tf.keras.layers.Dense(units=512, activation='relu', kernel_initializer='he_normal'),
   tf.keras.layers.Dropout(0.5),
   tf.keras.layers.Dense(units=256, activation='relu', kernel_initializer='he_normal'),
   tf.keras.layers.Dropout(0.5),
   tf.keras.layers.Dense(units=10, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Callbacks
early_stopping = tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5, min_lr=1e-7)

# Training with data augmentation
# history = model.fit(
#    datagen.flow(mnist_images.reshape(-1, 28, 28, 1), mnist_labels, batch_size=32),
#    epochs=50,
#    validation_data=(test_images.reshape(-1, 28, 28, 1), test_labels),
#    callbacks=[early_stopping, reduce_lr],
#    verbose=1
# )

# Evaluate on test set
# test_loss, test_accuracy = model.evaluate(test_images.reshape(-1, 28, 28, 1), test_labels, verbose=0)
# print(f"Test accuracy: {test_accuracy:.4f}")
# print(f"Test accuracy percentage: {test_accuracy*100:.2f}%")

# Save the model (saves architecture + weights + optimizer state)
# model.save('mnist_model.h5')

# OR save just the weights
# model.save_weights('mnist_weights.h5')