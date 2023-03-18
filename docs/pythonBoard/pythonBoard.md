
# Python Board 회고

> 함수형 View 를 사용해 만든 django 게시판

### 개발환경
- Python3.9
- Django4.1
- MySQL
- HTML, SCSS, Bootstrap
- jQuery

### 배포
- Naver Cloud Server
- Naver Cloud DB Server


## 기능 구현

### Naver Cloud DB Server MySQL 구축

AWS RDS를 통한 DB 구축은 여러번 해보았지만, Naver Cloud DB Server를 통한 DB 구축은 처음이었다.  
Naver Cloud DB Server 구축 자료는 많지 않았지만, 공식 문서가 보기 쉬웠다.

https://guide.ncloud-docs.com/docs/clouddbformysql-overview  
이 가이드를 참고하면 쉽게 구축할 수 있을 것이다.

아는 분이 AWS RDS가 해킹 당한 경우를 보면서 DB Password 키를 숨기는 중요성을 느꼈고 이번 프로젝트에도 적용하였다.

> setting.py
```python
import os.path, os, json
from django.core.exceptions import ImproperlyConfigured

# 중략 ...

secret_file = os.path.join(BASE_DIR.parent.parent, "key/.mysiteSecrets.json")   # *1

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured

SECRET_KEY = get_secret("SECRET_KEY")

# 중략 ...

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "pythonboard",
        "USER": get_secret("DATABASE_USER"),
        "PASSWORD": get_secret("DATABASE_PWD"),
        "HOST": get_secret("DATABASE_HOST"),
        "PORT": "3306",
        "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
    }
}

# 생략 ...

```
*1 이 코드의 경우 내가 django 프로젝트들을 한 번에 github에 올리다보니 BASE_DIR에서 두번이나 상위 폴더로 올라간 것이다.  
기본적으로 django 프로젝트를 github에 올린다면 

```python
secret_file = os.path.join(BASE_DIR, "key/.mysiteSecrets.json")   # *1
```
이렇게 구현하면 된다.

## login / logout

## CRUD

## 정렬

## pagination





### 
