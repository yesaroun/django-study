# 프로젝트 세팅

## 1. CRUD
Create : 생성  
Read : 조회  
Update : 수정  
Delete : 삭제

## 2. 프로젝트 생성 및 설정
```zsh
pyenv local django-envs
```
가상환경 실행

django 프로젝트 생성
```zsh
django-admin startproject costory
```

settings.py
```python
# TIME_ZONE = 'UTC'
# UTC는 국제 표준시를 나타냄
# Asia/Seoul로 수정하기
TIME_ZONE = 'Asia/Seoul'
```

```zsh
python manage.py startapp posts
```
posts라는 이름의 앱 생성  

settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
#         :
    'django.contrib.staticfiles',
    'posts',
]
```
posts 추가하기

```zsh
python manage.py migrate 
```
처음 세팅사항 반영하기  

## URL 구조
URL 구조를 미리 생각해두어야 구조적으로 잘 짜여진 프로젝트를 개발할 수 있다.  





