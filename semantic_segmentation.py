import numpy as np
from numpy import ndarray
from PIL import Image

from deeplab_model import Deeplabv3


# default normalization matches MobileNetV2
def generate_image_labels(image: ndarray, trained_image_width=512, mean_subtraction_value=127.5):
    # resize to max dimension of images from training dataset
    w, h, _ = image.shape
    ratio = float(trained_image_width) / np.max([w, h])
    resized_image = np.array(Image.fromarray(image.astype('uint8')).resize((int(ratio * h), int(ratio * w))))

    # apply normalization for trained dataset images
    resized_image = (resized_image / mean_subtraction_value) - 1.

    # pad array to square image to match training images
    pad_x = int(trained_image_width - resized_image.shape[0])
    pad_y = int(trained_image_width - resized_image.shape[1])
    resized_image = np.pad(resized_image, ((0, pad_x), (0, pad_y), (0, 0)), mode='constant')

    # make prediction
    deeplab_model = Deeplabv3()
    res = deeplab_model.predict(np.expand_dims(resized_image, 0))
    labels = np.argmax(res.squeeze(), -1)

    # resize back to original image
    labels = labels[:-pad_x]
    labels = np.array(Image.fromarray(labels.astype('uint8')).resize((h, w)))

    return labels