import os, base64, time
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from net import Model

model = Model()

app = Flask(__name__)

UPLOAD_FOLDER = './storage'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        img_base64 = request.form.get('imageData')
        img_jpg = base64.b64decode(img_base64)
        now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) 
        filename = now + '.jpg'
        filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file = open(filename, 'wb')
        file.write(img_jpg)
        file.close()

        pred_boxes, pred_class, pred_score = model.prediction(filename, 0.8)
        dict = {}
        dict['data'] = []
        for i in range(len(pred_boxes)):
            item = {
                'class': pred_class[i],
                'box': pred_boxes[i],
                'score': pred_score[i]
            }
            dict['data'].append(item)
        
        return jsonify(dict)
