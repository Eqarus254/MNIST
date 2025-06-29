# -*- coding: utf-8 -*- 7
"""MNIST Handwritten Digits.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Sh1Qsgp_MUVreTIDzkVUn_Z9axzegKWB
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

st.set_page_config(page_title="MNIST Classifier", layout="centered")

st.title("🧠 MNIST Digit Classifier")
st.write("This app uses a Convolutional Neural Network (CNN) to classify handwritten digits.")

# Load and preprocess the MNIST data
@st.cache_resource
def load_and_train_model():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # Normalize
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    # Reshape
    x_train = x_train.reshape(-1, 28, 28, 1)
    x_test = x_test.reshape(-1, 28, 28, 1)

    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    # Build the CNN
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation="relu"),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation="relu"),
        layers.Dense(10, activation="softmax")
    ])

    # Compile and train
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.1, verbose=0)

    # Evaluate
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)

    return model, x_test, y_test, test_acc

# Load and train
with st.spinner("Training model..."):
    model, x_test, y_test, test_acc = load_and_train_model()

st.success(f"✅ Model trained with test accuracy: {test_acc:.4f}")

# Slider to select number of predictions to display
num_images = st.slider("Number of test images to display", 1, 10, 5)

# Randomly select test images
indices = np.random.choice(len(x_test), num_images, replace=False)

fig, axs = plt.subplots(1, num_images, figsize=(num_images * 2, 2))

# Ensure axs is iterable
if num_images == 1:
    axs = [axs]

for i, idx in enumerate(indices):
    img = x_test[idx]
    true_label = np.argmax(y_test[idx])
    pred_label = np.argmax(model.predict(img.reshape(1, 28, 28, 1), verbose=0))

    axs[i].imshow(img.squeeze(), cmap="gray")
    axs[i].set_title(f"True: {true_label}\nPred: {pred_label}")
    axs[i].axis("off")

st.pyplot(fig)
