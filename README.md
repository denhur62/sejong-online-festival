# Sejong-Online-Festival
세종대학교 비대면 축제 서비스 플랫폼



## Dependency

- **python 3.6+**
- **Flask==2.0.1**
- **flask-validation-extended==0.1.5**
- **pymongo==3.11.4**
- **python-dotenv==0.17.1**



## Environment variable

```
SOF_MONGODB_NAME="SOF"
SOF_MONGODB_URI="mongodb://localhost:27017"
FLASK_APP="manage:application"
FLASK_CONFIG="development" # develop, production
FLASK_ENV="development" # develop, production
SOF_ERROR_LOG_PATH="./server.error.log"
SOF_PHOTO_UPLOAD_PATH="./app/asset/uploads"
SOF_SECRET_KEY="top-secret!!"
```



## Get Started

운영체제마다 세부적인 실행방법이 다를 수 있습니다. 

```shell
# Get Repository
$ git clone https://github.com/iml1111/IMFlask-Pymongo
$ cd IMFlask-Pymongo/

# virtual env
$ python3 -m venv venv
$ source ./venv/bin/activate

# Install dependency
$ pip install -r ./requirements/requirements.txt

$ cd IMFlask/

# DB init
$ flask db-init
[IMFlask] MongoDB Initialization Completed.

# App test
$ flask test
test_app_exists (test_basics.BasicsTestCase)
Application 검증 테스트 ... ok
...

# App start
$ flask run
```



##  Controller

- SejongAuth

```python
from controller.sejong_auth import SejongAuth

auth = SejongAuth()
id, pw = "16011089", "1234"
print(auth.do_sejong(id, pw))
print(auth.portal_sejong(id, pw))
```

