# mmaction에 있는 모델 flask로 배포하기 예제

- Flask는 Python으로 작성된 가벼운 웹 서버
- Pre-trained Pytorch model을 Flask 컨테이너로 감싸고 웹 API로 노출
- @app.route('/', methods=['GET’])으로 분류할 파일 요청
- @app.route('/predict', methods=['POST’]) 밑의 함수 코드로 결과값 생성
- 참고 demo: https://github.com/openmmlab/mmaction2/blob/master/demo/demo.ipynb
- Pytorch FLASK로 배포하기: https://tutorials.pytorch.kr/recipes/deployment_with_flask.html

```terminal
Anaconda environment in Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-193-generic x86_64)
conda create -n open-mmlab python=3.8
conda activate open-mmlab
pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html
pip3 install openmim
mim install mmcv-full
git clone https://github.com/open-mmlab/mmaction2.git
cd mmaction2
pip3 install -e .
```
버전에러 때문에 한 추가설치: ```conda install pillow=6.2.1```

배포를 위한 FLASK 사용을 위한 추가 설치: ```conda install -c anaconda flask```

Cf) 도커환경 구축 참고 사이트: https://mmaction2.readthedocs.io/en/latest/install.html#another-option-docker-image

## 배포한 app test
```terminal
FLASK_APP=app.py flask run
```
그러면 기본적으로 5000번 포트에서 수신대기(listen).

다른 터미널 창을 열어서 추론서버(inference server)를 테스트
```terminal
curl -X POST -H "Content-Type: multipart/form-data" http://localhost:5000/predict -F "file=@demo/demo.mp4;Type=video/mp4"
```

## 데이터셋과 모델 변경
- config_file, checkpoint_file, label에 해당하는 파일 다운받고 경로 지정
  + config_file은 configs/recognition/모델명 디렉토리에 다운
  + checkpoints 라는 디렉토리는 없으므로, 생성 후, 안에 다운받은 모델 weigh저장
  + label은 tools/data/데이터셋명 디렉토리에 존재. 맞춰서 경로 지정

## 파일을 모델에 넘겨주는 법
에러: ```RuntimeError: The type of argument video is not supported: <class'werkzeug.datastructures.FileStorage’>```

api 코드가 파일 스토리지에서 넘겨주는 데이터를 받는 기능은 구현을 안 해 놓았기 때문이었다. 그래서 파일을 저장한 다음에, 그 경로를 넘겨주는 식으로 했다. 경로를 넘겨줘서 받는 기능은 구현돼 있었다.
