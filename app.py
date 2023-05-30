import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from detection import AccidentDetectionModel

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
model = AccidentDetectionModel("model.json", 'model_weights.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(video_path)
            # Perform accident detection on the uploaded video
            result = model.detect_accident(video_path)
            return render_template('upload.html', result=result)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run()
