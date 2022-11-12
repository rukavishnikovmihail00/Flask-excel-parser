import os

from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, send_file, render_template
from parser import parse

UPLOAD_FOLDER = 'uploads/'
TMP_FOLDER = 'tmp/'

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TMP_FOLDER'] = TMP_FOLDER


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if not os.path.exists('uploads'):
            os.mkdir('uploads')
        if not os.path.exists('tmp'):
            os.mkdir('tmp')

        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_filename = parse(os.path.join(app.config['UPLOAD_FOLDER'], filename), app.config['TMP_FOLDER'])
            return redirect('/download/' + new_filename)

    return render_template('upload.html')


@app.route("/download/<new_filename>", methods=['GET'])
def download_file(new_filename):
    return render_template('download.html', value=new_filename)


@app.route('/return/<filename>')
def return_file(filename):
    return send_file(os.path.join(app.config['TMP_FOLDER'], filename), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
