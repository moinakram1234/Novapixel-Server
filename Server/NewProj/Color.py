import os
import glob
import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt

def get_image_paths(dataset_path):
    file_paths = glob.glob(os.path.join(dataset_path, '*.jpg'))
    return file_paths

def get_dominant_color(image, k=3):
    image = cv2.resize(image, (50, 50), interpolation=cv2.INTER_AREA)
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    
    clt = KMeans(n_clusters=k)
    labels = clt.fit_predict(image)

    label_counts = np.bincount(labels)
    dominant_color = clt.cluster_centers_[np.argmax(label_counts)]
    
    return dominant_color / 255

def color_distance(color1, color2):
    return np.sqrt(np.sum((color1 - color2) ** 2))

def display_images(images, titles):
    plt.figure(figsize=(15, 5))
    for i, image in enumerate(images):
        plt.subplot(1, len(images), i+1)
        plt.imshow(image)
        plt.title(titles[i])
        plt.axis('off')
    plt.show()
def main():
    input_image_path = "NewProj/input_image.jpg"

    try:
        input_image = cv2.imread(input_image_path)
        if input_image is None:
            raise FileNotFoundError

        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        target_color = get_dominant_color(input_image)

    except FileNotFoundError:
        print("Invalid image file path.")
        return

    dataset_path = "Images"
    image_file_paths = get_image_paths(dataset_path)

    matching_images = []

    for image_path in image_file_paths:
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        dominant_color = get_dominant_color(image)

        if np.array_equal(dominant_color, target_color):
            matching_images.append(image)

    if matching_images:
        display_images(matching_images, [f"Image {i+1}" for i in range(len(matching_images))])
    else:
        print("No matching images found.")

if __name__ == "__main__":
    main()
