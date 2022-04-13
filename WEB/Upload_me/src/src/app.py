# -*- coding: utf-8 -*-
from flask import Flask, render_template,redirect, url_for, request, Response
import uuid
import random
from werkzeug.utils import secure_filename
import os
random.seed(uuid.getnode())
app = Flask(__name__)
app.config['SECRET_KEY'] = str(random.random()*100)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024
ALLOWED_EXTENSIONS = set(['zip'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET','POST'])
def index():
    error = request.args.get('error', '')
    if error == '1':
        return render_template('index.html', forbidden=1)
    return render_template('index.html')


@app.route('/upload', methods=['POST','GET'])
def upload_file():
    if 'the_file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['the_file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if(os.path.exists(file_save_path)):
            return 'This file already exists'
        file.save(file_save_path)
    else:
        return 'This file is not a zipfile'

    extract_path = file_save_path + '_'
    file = ''
    os.system('unzip -n ' + file_save_path + ' -d '+ extract_path)
    dir_list = os.popen('ls ' + extract_path, 'r').read()
    print(dir_list.split())
    for dir in dir_list.split():
        if '../' in dir:
            os.system('rm -rf ' + extract_path)
            os.remove(file_save_path)
            return redirect(url_for('index', error=1))
        file += open(extract_path + '/' + dir, 'r').read()
    os.system('rm -rf ' + extract_path)
    os.remove(file_save_path)

    return Response(file)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=10008)








