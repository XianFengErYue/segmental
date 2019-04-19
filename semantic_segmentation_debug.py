from semantic_segmentation import generate_image_labels

from PIL import Image
from matplotlib import pyplot as plt
import numpy as np


input_image = '/Users/Ben/PycharmProjects/segmental/test/test_images/cat.jpg'

img_array = np.array(Image.open(input_image))

result = generate_image_labels(img_array)

plt.imshow(result)
plt.waitforbuttonpress()