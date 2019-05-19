import os

from flask import Flask, request, jsonify
import numpy as np
from PIL import Image

from segmentation.segmentation_utils import generate_image_labels
from authentication.api_key_utils import get_api_key_from_s3


# Disable annoying TensorFlow Logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)


def allowed_file_type(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    if extension in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


@app.route('/generate_labels', methods=['POST'])
def segmental_endpoint():
    headers = request.headers
    if "x-api-key" not in headers:
        return "An API Key is required", 403

    auth = headers.get("x-api-key")

    if auth == get_api_key_from_s3():
        if 'image' not in request.files:
            return "An image file is required", 400

        image = request.files['image']

        if image.filename == '':
            return "An image file is required", 400

        if image and allowed_file_type(image.filename):
            image = np.array(Image.open(image))
            result = generate_image_labels(image)

            return jsonify({'labels_array': result.tolist()})
        else:
            return f"Invalid file extension, allowed extensions are {ALLOWED_EXTENSIONS}", 400
    else:
        return "Invalid API Key", 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

