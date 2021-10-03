# 😀세종대학교 비대면 축제 서비스 플랫폼
![image-20211003204322170](https://user-images.githubusercontent.com/47492535/135700436-46eab051-4784-4b10-8c27-2b8ed7f3d43b.png)



## 😄프로젝트 배경 / 소개

첫번째, 갑작스러운 언택트 시대의 도래로 학교의 축제들이 힘을 잃어 감에 따라 학생들의 소속감이 저하되고 있습니다. 저희들은 해당 프로젝트를 통해 저희 학교 축제의 불빛을 되찾고자 합니다.

두번째는 교내 체계적인 축제 운영 시스템의 부재입니다. 학생회 및 동아리는 축제에 대한 산발적인 홍보로 인하여 몇몇 학생들에게 정보가 닿지 않는일이 다반사이며, 몇몇 행사들은 참가자 외에는 구경조차 하기 어려워 그들만의 리그가 되곤 했습니다.

때문에 저희는 기존 세종대학교 축제의 문제점들을 개선하고 언택트 시대에 걸맞는 온라인 축제 플랫폼을 기획하게 되었습니다.

저희들이 이 프로젝트를 통해 목표로 하는 것은 다음과 같습니다.

첫번째 , 저희는 많은 학생들이 주도적으로 축제에 참여할 수 있는 플랫폼을 만들고자 합니다. 현재 학생회나 동아리에 소속되어 있지 않은 학생들은 부스를 만드는 등 축제에 주도적인 참여가 불가능합니다.  하지만 저희 플랫폼을 통해서 개인으로도 축제에 참여 할 기회를 제공받는다면 스스로 축제를 직접 참여하고 기여하여 더욱 열정적으로 축제에 몰입할 수 있을 것 입니다.

두번째로는 채팅, 응원하기, 방명록 등 학생들간의 소통 공유를 최대한 이끌어 낼 수 있는 서비스를 구현함으로써 비대면으로 무뎌진 소속감을 끌어 올릴 수 있는 플랫폼을 구축하는 것이 목표입니다.



## 📈Dependency

- **python 3.6+**
- **Flask==2.0.1**
- **flask-validation-extended==0.1.5**
- **pymongo==3.11.4**
- **python-dotenv==0.17.1**



## 📈Environment variable
SOF_PHOTO_UPLOAD_PATH는 static URL을 사용하기 위해, app/asset/ 내에 지정하는 걸 추천.

```
SOF_MONGODB_NAME="SOF"
SOF_MONGODB_URI="mongodb://localhost:27017"
FLASK_APP="manage:application"
FLASK_CONFIG="development" # develop, production
FLASK_ENV="development" # develop, production
SOF_ERROR_LOG_PATH="./server.error.log"
SOF_PHOTO_UPLOAD_PATH="./app/asset/uploads"
SOF_SECRET_KEY="top-secret"
SOF_ADMIN_ID="admin"
SOF_ADMIN_PW="1234"
```



## 📈Get Started

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

