import json
import os
import sys
import time
import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from keras.models import Model
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import base64

#model....................................................
def download_image(url, save_as):
    try:
        # Decode the base64 encoded string to bytes
        image_data = base64.b64decode(url.split(",")[1])
        
        # Save the decoded bytes to a file
        with open(save_as, 'wb') as f:
            f.write(image_data)
            
        print(f'Successfully saved file as {save_as}')
    except Exception as e:
        print(f'An error occurred: {e}')


def get_image_paths(dataset_path):
    file_paths = glob.glob(os.path.join(dataset_path, '*.jpg'))
    return file_paths

import matplotlib.pyplot as plt
import time

def display_images(images, titles, filenames):
     for i, image in enumerate(images):
        print(f"https://cdn.shopify.com/s/files/1/0722/2254/0097/products/{filenames[i]}?v={int(time.time())}")


def load_and_preprocess_image(image_path):
    img = Image.open(image_path).resize((224, 224))
    img_data = np.array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    return img_data

def extract_features(img_data, model):
    features = model.predict(img_data)
    return features

def main():
# download input image from Arguments......................
    try:
         json_str = sys.argv[1]
    except IndexError:
         print("Please provide a JSON string as an argument.")
         sys.exit(1)

    try:
    # Parse the JSON string into a Python object
         my_object = json.loads(json_str)
    except json.JSONDecodeError:
          print("The provided argument is not a valid JSON string.")
          sys.exit(1)

    other_image_url = my_object.get('imageData')
    if other_image_url is None:
         print('Failed to read other image')
         sys.exit(1)

    save_as = "NewProj/input_image.jpg"
    download_image(other_image_url, save_as)


    input_image_path = save_as
    try:
        input_image = cv2.imread(input_image_path)
        if input_image is None:
            raise FileNotFoundError

        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    except FileNotFoundError:
        print("Invalid image file path.")
        return

    dataset_path = "Images"
    image_file_paths = get_image_paths(dataset_path)

    base_model = MobileNetV2(weights='imagenet', include_top=True)
    feature_extractor = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)

    input_image_data = load_and_preprocess_image(input_image_path)
    input_image_features = extract_features(input_image_data, feature_extractor)

    matching_scores = []

    for image_path in image_file_paths:
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image_data = load_and_preprocess_image(image_path)
        image_features = extract_features(image_data, feature_extractor)

        similarity_score = cosine_similarity(input_image_features, image_features)[0][0]
        matching_scores.append((similarity_score, image_path))

    matching_scores.sort(reverse=True, key=lambda x: x[0])
    top_3_images = [score_image[1] for score_image in matching_scores[:3]]

    if top_3_images:
       image_filenames = [os.path.basename(image_path) for image_path in top_3_images]
       display_images(top_3_images, [f"Image {i+1}" for i in range(len(top_3_images))], image_filenames)
    else:
       print("No matching images found.")



if __name__ == "__main__":
    main()
