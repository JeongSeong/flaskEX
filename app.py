# app.py 
# mmaction2 디렉토리 안에 저장

from mmaction.apis import init_recognizer, inference_recognizer
from flask import Flask, jsonify, request

app = Flask(__name__)

config_file = 'configs/recognition/tsn/tsn_r50_video_inference_1x1x3_100e_kinetics400_rgb.py'
# download the checkpoint from model zoo and put it in `checkpoints/`
checkpoint_file = 'checkpoints/tsn_r50_1x1x3_100e_kinetics400_rgb_20200614-e508be42.pth'
# build the model from a config file and a checkpoint file
model = init_recognizer(config_file, checkpoint_file, device='cuda')

model.eval()       

label = 'tools/data/kinetics/label_map_k400.txt'
labels = open(label).readlines()
labels = [x.strip() for x in labels]

@app.route('/', methods=['GET'])
def root():
    return jsonify({'msg' : 'Try POSTing to the /predict endpoint with an mp4 video attachment'})

from werkzeug.utils import secure_filename
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file'] # <FileStorage: 'demo.mp4' ('application/octet-stream')>
        if file is not None:
            filename = secure_filename(file.filename)
            file.save(filename)
            results = inference_recognizer(model, filename)
            results = {labels[k[0]]: float(k[1]) for k in results}
            return jsonify(results)

if __name__ == '__main__':
    app.run()