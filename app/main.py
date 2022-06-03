from operator import imod
from flask import Flask, render_template, jsonify, make_response, request
from .utils import allowed_file
from .segmentation import Segmentation
import cv2
import numpy as np
import io
from base64 import encodebytes, b64encode

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/do-segmentation', methods=['POST'])
def do_segmentation():
    if 'input-file' not in request.files:
        return make_response(jsonify({'msg': 'No File Part'}), 400)

    input_img = request.files.get('input-file')

    if input_img.filename == '':
        return make_response(jsonify({'msg': 'No File Part'}), 400)
    if input_img and allowed_file(input_img.filename):
        face_part = request.form.get('seg-part')
        face_part = face_part if face_part != '' else 'all'
        file_ext = input_img.filename.split('.')[-1]

        FaceSegmentation = Segmentation()
        img = FaceSegmentation.do_segmentation_chain(img=input_img, part=face_part, file_ext=file_ext)
        
        return make_response(jsonify({'msg': 'Test', 'img': img, 'format': file_ext}))
    else:
        return make_response(jsonify({'msg': 'File type not allowed'}), 400)