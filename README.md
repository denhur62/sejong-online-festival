# Sejong-Online-Festival
세종대학교 비대면 축제 서비스 플랫폼



## Dependency

- **python 3.6+**
- **Flask==2.0.1**
- **flask-validation-extended==0.1.5**
- **pymongo==3.11.4**
- **python-dotenv==0.17.1**



## Environment variable

어플리케이션을 실행하기 위해서는 아래와 같은 환경 변수 설정이 필요합니다.

dotenv 라이브러리를 위해 config.py와 같은 경로에 .env 파일을 작성하셔도 되고, 직접 환경변수를 입력하셔도 상관없습니다.

- **SOF_MONGODB_NAME**=MongoDB DB Name

  MongoDB 서버에 접속하기 위한 Database Name 입니다.

- **SOF_MONGODB_URI**=MongoDB URI
  MongoDB 서버에 접속하기 위한 Database URI입니다.

- **SOF_ERROR_LOG_PATH**=Server_Error_log Path
  에러를 기록할 별도의 로그 경로입니다.

- **FLASK_APP**="manage:application"
  Flask APP 객체의 위치를 가리키는 값입니다. 

- **FLASK_CONFIG**=Config type # development or production
  어떤 config 데이터를 주입시킬지 결정하는 값입니다.

- **FLASK_ENV**=# development or production
  어떠한 환경에서 Flask APP을 실행시킬지 결정하는 값입니다. 



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

