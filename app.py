import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# @app.route('/name', methods=['GET', 'POST'])
# def js_call():
#     if request.method == 'POST':
#         first_name = request.json['first_name']
#         last_name = request.json['last_name']
#         print("{} {}".format(first_name, last_name))
#         return jsonify({'status': 'Received'})
#     if request.method == 'GET':
#         t = {'status': 'Sent'}
#         return jsonify(t)


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
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
            message = {"Status": "Uploaded"}
            return jsonify(message)