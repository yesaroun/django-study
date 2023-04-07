
## 목차

- [Python Board 요약](https://github.com/yesaroun/django-study/tree/main/doit/mysite#python-board-요약)
- [기능 정리](https://github.com/yesaroun/django-study/tree/main/doit/mysite#기능-정리)
- [모델](https://github.com/yesaroun/django-study/tree/main/doit/mysite#모델)
- [장고 Admin](https://github.com/yesaroun/django-study/tree/main/doit/mysite#장고-admin-사용하기)
- [질문 목록 조회(https://github.com/yesaroun/django-study/tree/main/doit/mysite#질문-목록-조회-구현하기)
- [질문 상세 기능](https://github.com/yesaroun/django-study/tree/main/doit/mysite#질문-상세-기능-구현하기)
- [오류 화면](https://github.com/yesaroun/django-study/tree/main/doit/mysite#오류-화면-구현하기)
- [URL 별칭](https://github.com/yesaroun/django-study/tree/main/doit/mysite#url-별칭으로-url-하드-코딩-문제-해결하기)
- [URL namespace](https://github.com/yesaroun/django-study/tree/main/doit/mysite#url-네임스페이스-알아보기)
- [스타일 시트 적용](https://github.com/yesaroun/django-study/tree/main/doit/mysite#웹-페이지에-스타일-시트-적용하)
- [get_object_or_404](https://github.com/yesaroun/django-study/tree/main/doit/mysite#get_object_or_404)
- [view 파일 분리](https://github.com/yesaroun/django-study/tree/main/doit/mysite#1-viewspy-파일-분리하기)

# Python Board 요약

> 함수형 View 를 사용해 만든 django 게시판

### 개발환경
- Python3.9
- Django4.1
- MySQL
- HTML, SCSS, Bootstrap
- jQuery

# 기능 정리

# 모델

### migrate 실행 명령

```bash
python manage.py migrate
```

## 모델 생성

pybo/models.py

```python
from django.db import models

# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)  # 글자 수 제한하고 싶은 경우 CharField()
    content = models.TextField()                # 글자 수 제한이 없는 경우 TextField()
    create_date = models.DateTimeField()        # 날짜, 시간 관련 속성

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # ForeingKey : ForeingKey 지정
    # on_delete=models.CASCADE : 답변에 연결된 질문이 삭제되면 답변도 함께 삭제하라는 의미
    content = models.TextField()
    create_date = models.DateTimeField()
```

테이블을 생성하려면 config/settings.py 파일에 INSTALLED_APPS 항목에 pybo 앱 추가

```python
INSTALLED_APPS = [
    'pybo.apps.PyboConfig',    # 추가
    'django.contrib.admin',
		# (... 생략 ...)
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

'pybo.apps.PyboConfig' : pybo/apps.py 안에 PyboConfig 클래스
pybo 앱을 만들 때 자동으로 생성된 것이다.

```python
from django.apps import AppConfig

class PyboConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pybo'
```

중요한 점은 PyboConfig 클래스가 config/settings.py 파일의 INSTALLED_APPS 항목에 추가되지 않으면 장고는 pybo앱을 인식하지 못하고 데이터베이스 관련 작업도 할 수 없다는 점이다. 
장고는 모델을 이용하여 데이터베이스의 실체가 될 테이블을 만드는데, 모델은 앱에 종속되어 있으므로 반드시 장고에 앱을 등록해야 테이블 작업을 진행할 수 있다. 

이렇게 진행하고 테이블 생성을 위해 migrate 명령어를 실행해야 한다.

```bash
python manage.py migrate
```

하지만 migrate 명령이 제대로 수행되지 않는다. 왜냐하면 모델이 생성되거나 변경된 경우 migrate 명령을 실행하려면 테이블 작업 파일이 필요하고, 테이블 작업 파일을 만들려면 makemigrations 명령을 실행해야 한다.

```bash
python manage.py makemigrations
```

이후에 migrate 명령을 수행한다.

migrate 명령을 실행할 때 수행되는 쿼리문 확인

```bash
python manage.py sqlmigrate pybo 0001
```

‘pybo’는 makemigrations 명령을 실행할 때 생성된 pybo/migrations/0001_initial.py의 마이그레이션명 ‘pybo’를 의미
’0001’은 생성된 파일의 일련번호를 의미

## 모델 사용(데이터 만들고 저장하고 조회하기)

#### 장고 셸 실행하기

장고 셸은 파이썬 셸과 비슷하지만 장고에 필요한 환경들이 자동으로 설정되어 실행된다.

```bash
python manage.py shell
```

### Question, Answer 모델 임포트하기

```bash
from pybo.models import Question, Answer
```

### Question 모델로 Question 모델 데이터 만들기

```python
from django.utils import timezone
q = Question(subject='pybo가 무엇인가요?', content='pybo에 대해 알고 싶습니다.', create_date=timezone.now())
```

timezone.now() : 현재 일시 입력
이 과정을 통해 객체 q가 생성된다. 객체가 생성된 다음 q.save()를 입력하면 Question 모델 데이터 1건이 DB에 저장된다.

### Question 모델 데이터의 id값 확인하기

```python
q.id
#--==>> 1
```

id는 PK(primary key)이다.

## Question 모델 데이터 모두 조회하기

```python
Question.objects.all()
#--==>> <QuerySet [<Question: Question object (1)>, <Question: Question object (2)>, <Question: Question object (3)>]>
```

장고에서 저장된 모델 데이터는 Question.objects를 사용해 조회할 수 있다.
<Question object (1)>의 1이 장고에서 Question 모델 데이터에 자동으로 입력해 준 id이다.

## Question 모델 데이터 조회 결과에 속성값 보여 주기

Question 모델에 **str** 메서드를 추가하면 된다.

pybo/models.py

```python
# (생략)

class Question(models.Model):
    subject = models.CharField(max_length=200)  
    content = models.TextField()                
    create_date = models.DateTimeField()        

    def __str__(self):
        return self.subject

# (생략)
```

다만, 모델이 수정될 경우 quit() 명령을 수행해서 장고 셸을 종료한 다음 다시 시작하고, Question 모델을 다시 임포트한 후 Question 모델을 다시 조회해야 한다.

```python
from pybo.models import Question, Answer
Question.objects.all()
#--==>> <QuerySet [<Question: pybo가 무엇인가요?>, <Question: 장고 모델 질문입니다.>, <Question: pybo가 무엇인가요?>]>
```

참고로, **makemigrations, migrate 명령은 모델의 속성이 추가되거나 변경된 경우 실행하는 명령이다.** 그래서 지금은 메서드가 추가된 것이므로 이 과정은 하지 않아도 된다.

## 조건으로 Question 모델 데이터 조회하기

```python
Question.objects.filter(id=1)
#--==>> <QuerySet [<Question: pybo가 무엇인가요?>]>
```

다만, filter 함수는 반환값이 리스트 형태인 QuerySet이므로 정말로 1개의 데이터만 조회하고 싶다면, filter 함수 대신 get 함수를 쓰는 것이 좋다.

```python
Question.objects.get(id=1)
#--==>> <Question: pybo가 무엇인가요?>
```

filter 함수는 여러 건의 데이터를 반환하지만, get함수는 단 한 건의 데이터를 반환한다.
또한 get 함수는 반드시 1건의 데이터를 반환해야 한다는 특징이 있다.
그래서 get으로 존재하지 않는 데이터를 조회하면 error가 나고, filter함수로 존재하지 않는 데이터를 조회하면 빈 QuerySet을 반환한다.(<QuerySet []>)

## 제목의 일부를 이요하여 데이터 조회하기

__contains를 이용하면 문자열이 포함된 데이터를 조회할 수 있다.

```python
Question.objects.filter(subject__contains='장고')
#--==>> <QuerySet [<Question: 장고 모델 질문입니다.>]>
```

## 데이터 수정하기

### Question 모델 데이터 수정하기

```python
q = Question.objects.get(id=2)
q
#--==>> <Question: 장고 모델 질문입니다.>
q.subject = 'Django Model Question'
# subject 속성 수정
q.save()
q
#--==>> <Question: Django Model Question>
```

## 데이터 삭제하기

### Question 모델 데이터 삭제하기

```python
q = Question.objects.get(id=1)
q.delete()
#--==>> (1, {'pybo.Question': 1})
```

delete() 함수를 수행하면 해당 데이터가 DB에서 삭제되고, 삭제된 데이터의 추가 정보가 반환된다. 1은 Question 모델 데이터의 id를 의미하고, {’pybo.Question’: 1}은 삭제된 모델의 데이터의 개수를 의미한다.
Answer 모델을 만들 때 ForeignKey로 Question 모델했기에 만약 삭제한 Question 모델 데이터에 2개의 Answer 모델 데이터가 등록된 상태라면 (1, {’pybo.Answer’: 2,’pybo.Question’:1 })와 같이 삭제된 답변 개수도 반한될 것이다.

## 연결된 데이터 알아보기

Answer 모델은 Question 모델과 연결되어 있으므로(ForeignKey) 데이터를 만들 때 Question 모델 데이터가 필요하다.

### Answer 모델 데이터 만들기

```python
>>> Question.objects.get(id=2)
<Question: Django Model Question>
>>> q = Question.objects.get(id=2)
>>> q
<Question: Django Model Question>
>>> from django.utils import timezone
>>> a = Answer(question=q, content='네 자동으로 생성됩니다.', create_date=timezone.now())
>>> a.save()
```

Answer 모델 데이터에도 id가 있다.

```python
>>> a.id
1
```

### Answer 모델 데이터 조회하기

```python
>>> a = Answer.objects.get(id=1)
>>> a
<Answer: Answer object (1)>
```

### 연결된 데이터로 조회하기: 답변에 있는 질문 조회하기

Answer 모델 데이터에는 Question 모델 데이터가 연결되어 있으므로 Answer 모델 데이터에 연결된 Question 모델 데이터를 조회할 수 있다.

```python
>>> a.question
<Question: Django Model Question>
```

### 연결된 데이터로 조회하기: 질문을 통해 답변 찾기

Answer 모델 객체인 a에는 question 속성이 있으므로 a를 통해 질문을 찾는 것이 쉽다.
Question 모델에는 답변 속성이 없지만 answer_set을 사용하면 찾을 수 있다.

```python
>>> q.answer_set.all()
<QuerySet [<Answer: Answer object (1)>]>
```

Question 모델과 Answer 모델처럼 서로 연결되어 있으면 **연결모델명_set** 과 같은 방법으로 연결된 데이터를 조회할 수 있다.

# 장고 Admin 사용하기

장고 Admin을 사용하려면 super user를 먼저 생성해야 한다. super user는 장고 운영자 계정이라고 생각하면 된다.

## 슈퍼 유저 생성하기

```python
% python manage.py createsuperuser
Username (leave blank to use 'akor1'): admin
Email address: akor1@naver.com  
Password: 1234
Password (again): 1234
This password is too short. It must contain at least 8 characters.
This password is too common.
This password is entirely numeric.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

실제 사이트를 운영한다면 보안에 취약한 비밀번호를 사용해서는 안된다.

[localhost:8000/admin](http://localhost:8000/admin) 에 접속하고 로그인하면 관리자 페이지 나온다.

## 장고 Admin에서 모델 관리하기

모델들을 장고 Admin에 등록하면 손쉽게 모델을 관리할 수 있다. 이전에 장고 셸에서 수행했던 작업을 장고 Admin에서 할 수 있다. 

pybo/admin.py

```python
from django.contrib import admin
from .models import Question

admin.site.register(Question)
```

이렇게 작성하고 장고 Admin으로 Question 모델이 추가되어 있다. 그러면 셸이 아닌 장고 Admin 화면에서 Question 모델을 직관적으로 관리할 수 있다.

## 장고 Admin에 데이터 검색 기능 추가하기

pybo/admin.py

```python
from django.contrib import admin
from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)
```

제먹을 검색할 수 있도록 검색 항목을 추가했다. QuestionAdmin 클래스를 추가하고 search_fields에 ‘subject’를 추가했다.
그러면 장고 Admin을 새로고침하면 검색 기능이 추가되었다.

파이보의 핵심 기능인 질문 목록과 질문 상세 기능을 구현해보겠다.

# 질문 목록 조회 구현하기

## Question 모델 데이터 작성일시 역순으로 조회하기

Question 모델을 임포트해 Question 모델 데이터를 작성한 날짜의 역순으로 조회하기 위해 order_by 함수를 사용했다. 조회한 Question 모델 데이터는 context 변수에 저장했다. context 변수는 render 함수가 템플릿을 HTML로 변환하는 과정에서 사용되는 데이터이다.
order_by함수는 조회한 데이터를 특정 속성으로 정렬하며, ‘-create_date’는 - 기호가 앞에 붙어 있으므로 작성일시의 역순을 의미한다. 

```python
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

def index(request):
    """pybo 목록 출력"""
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)
```

render 함수는 context에 있는 Question 모델 데이터 question_list를 pybo/question_list.html 파일에 적용하여 HTML 코드로 변환한다. 장고에서는 이런 파일을 템플릿이라고 부른다.

이후 루트 디렉터리 밑에 templates 디렉터리를 생성한다. 이 디렉터리에 템플릿을 모아 관리한다.

템플릿 디렉터리를 장고 mysite/settings.py 파일에 등록해야 한다.
settings.py

```python
TEMPLATES = [
		{
				(생략)
				'DIRS': [BASE_DIR / 'templates'],
				(생략)
		},
]
```

DIRS에는 템플릿 디렉터리를 여러 개 등록할 수 있다. 다만 현재는 1개의 템플릿 디렉터리를 쓸 것이여서 위와 같이 등록한다.
BASE_DIR 은 루트 디렉터리의 경로여서 뒤에 ‘templates’만 붙인다. 

참고로 장고는 앱 하위에 있는 templates 디렉터리를 자동으로 템플릿 디렉터리로 인식한다. 하지만 이 방법은 권장하지 않는다. 왜냐하면 하나의 사이트에서 여러 앱을 사용할 때 여러 앱의 화면을 구성하는 템플릿은 한 디렉터리에 모아 관리하는 편이 여러모로 좋기 때문이다.
그래서 파이보는 템플릿 디렉터리를 mysite/pybo/templates와 같은 방식이 아니라, mysite/templates/pybo 와 같은 방식으로 관리한다.

## 템플릿 파일 만들기

templates/pybo/question_list.html

```html
{% if question_list %}
  <ul>
    {% for question in question_list %}
      <li><a href="/pybo/{{ question.id }}">{{ question.subject }}</a></li>
    {% endfor %}
  </ul>
{% else %}
  <p>질문이 없습니다.</p>
{% endif %}
```

작성한 이후 서버를 다시 시작하고 /pybo/에 접송하면 보인다.

템플릿 태그는 {% %}로 둘러싸였다. 

### 템플릿 태그

| 템플릿 태그 | 의미 |
| --- | --- |
| {% if question_list %} | question_list가 있다면 |
| {% for question in question_list %} | question_list를 반복하며 순차적으로 question에 대입 |
| {{ http://question.id }} | for 문에 의해 대입된 question 객체의 id 출력 |
| {{ question.subject }} | for 문에 의해 대입된 question 객체의 subject 출력 |

## 템플릿 태그 3가지 유형

### if

```python
{% if 조건문1 %}
  <p>조건문1에 해당하는 경우</p>
{% elif 조건문2 %}
  <p>조건문2에 해당하는 경우</p>
{% else %}
  <p>else 경우</p>
{% endif %}     endif 중요!!
```

### for

```python
{% for item in list %}
  <p>순서: {{ forloop.counter }}</p>
  <p>{{ item }}</p>
{% endfor %}    endfor 중요!
```

### forloop 객체

forloop객체는 반복 중 유용한 값을 제공한다.

| forloop 객체 속성 | 설명 |
| --- | --- |
| forloop.counter | for 문의 순서로 1부터 표시 |
| forloop.counter0 | for 문의 순서로 0부터 표시 |
| forloop.first | for 문의 첫 번째 순서인 경우 True |
| forloop.last | for 문의 마지막 순서인 경우 True |

### 객체

객체 속성은 파이썬과 동일한 방법으로 점(.)연산자 사용

```python
{{ question }}
{{ question.id }}
{{ question.subject }}
```

# 질문 상세 기능 구현하기

현재 구현한 페이지에서 질문을 누르면 404 오류가 나온다. 왜냐하면 pybo/2 에 대한 URL 매핑을 추가하지 않았기 때문이다.

## pybo/urls.py URL 매핑 추가하기

pybo/urls.py

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('<int:question_id>/', views.detail),   # 추가
]
```

question_id에 2라는 값이 저장된고 views.detail 함수가 실행된다.

## pybo/views.py에 화면 추가하기

```python
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

def index(request):
    """pybo 목록 출력"""
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

# 추가
def detail(request, question_id):
    """pybo 내용 출력"""
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
```

detail 함수는 index함수와 크게 다르지 않다. 다만, detail 함수의 매개변수 question_id가 추가 되었고 이것이 바로 URL 매핑에 있던 question_id이다.

### 정리

localhost:8000/pybo/2 입력 → mysite/urls.py에서 pybo/ 매핑 → pybo/urls.py에서 2/를 매핑(<int:question_id>에 2 매핑) → pybo/views.py의 detail 함수의 매개변수로 question_id로 2가 전달

## pybo/question_detail.html 작성하기

templates/pybo/question_detail.html

```html
<h1>{{ question.subject }}</h1>

<div>
  {{ question.content }}
</div>
```

이후 /pybo/2/에 접속하면 질문 상세 화면이 나타난다.

# 오류 화면 구현하기

/pybo/39/ 와 같이 잘못된 주소로 접속하면 “DoesNotExist” 오류 화면이 나온다.
question_id가 30인 데이터를 조회하는 Question.object.get(id=30)에서 오류가 발생했기 때문이다.

### 정리

[localhost:8000/pybo/30/](http://localhost:8000/pybo/30/) 입력 → mysite/urls.py에서 pybo/ 매핑 → pybo/urls.py에서 30/ 매핑 → pybo/views.py의 detail의 함수 매개 변수 question_id로 30이 전달 되고 이후 Question.object.get(id=30)에서 오류 발생

## 404페이지 출력하기

detail 함수에서 Question.objects.get(id=question_id)를 get_object_or_404(Question, pk=question_id)로 수정하면 된다.

pybo/views.py

```python
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Question

def index(request):
    """pybo 목록 출력"""
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """pybo 내용 출력"""
    question = get_object_or_404(Question, pk=question_id) # 수정
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
```

이렇게 수정하면 존재하지 않는 페이지에서 404 페이자가 뜬다.

### 오류 코드

| 오류 코드 | 설명 |
| --- | --- |
| 1XX(정보) | 요청을 받았으며 프로세스를 계속 진행 |
| 2XX(성공) | 요청을 성공적으로 받았으며 인식했고 수용 |
| 3XX(리다이렉션) | 요청 완료를 위해 추가 작업 조치가 필요 |
| 4XX(클라이언트 오류) | 요청의 문법이 잘못되었거나 요청을 처리할 수 없슴 |
| 5XX(서버 오류) | 서버가 명백히 유효한 요청에 대한 충족을 실패 |


기존 question_list.html 템플릿에서 사용된 href를 보면
```python
<li><a href="/pybo/{{ question.id }}">{{ question.subject }}</a></li>
```
이러한 URL규칙을 사용했다. 하지만 이런 URL 규칙은 프로그램을 수정하면서 ‘/pybo/question/2/’ 또는 ‘/pybo/2/question/’으로 수정될 가능성도 있다. 이렇게 URL 규칙이 자주 변경된다면 템플릿에 사용된 모든 href 값들을 일일이 찾아 수정해야 한다. 
이게 URL 하드 코딩의 한계이다.
이런 문제를 해결하려면 해당 URL에 대한 실제 주소가 아닌 주소가 매핑된 URL 별칭을 사용해야 한다.


# URL 별칭으로 URL 하드 코딩 문제 해결하기

## pybo/urls.py 수정하여 URL 별칭 사용하기
pybo/urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # 수정
    path('<int:question_id>/', views.detail, name='detail'),  # 수정
]
```
path 함수에 있는 URL 매핑에 name 속성을 부여했다. 이렇게 수정하면 실제 주소 /pybo/ 는 index라는 URL 별칭이, /pybo/2/는 detail이라는 URL 별칭이 생긴다.

## pybo/question_list.html 템플릿에서 URL 별칭 사용하기
앞에서 만든 별칭을 템플릿에서 사용하기 위해 /pybo/{{ question.id }}를 {% url 'detail' question.id %}로 수정한다.
mysite/templates/pybo/question_list.html
```html
{% if question_list %}
  <ul>
    {% for question in question_list %}
      <li><a href="{%  url 'detail' question_id %}">{{ question.subject }}</a></li>   <!-- 수정 -->
    {% endfor %}
  </ul>
{% else %}
  <p>질문이 없습니다.</p>
{% endif %}
```

# URL 네임스페이스 알아보기
현재는 프로젝트에서 pybo 앱 하나만 사용하지만, 이후 pybo 앱 이외의 다른 앱이 프로젝트에 추가될 수도 있다.
이때 서로 다른 앱에서 같은 URL 별칭을 사용하면 중복 문제가 생긴다.

이 문제를 해결하기 위해 pybo/urls.py 파일에 네임스페이스(namespace)라는 개념을 도입해야 한다.
namespace : 각각의 앱이 관리하는 독립된 이름 공간

## pybo/urls.py에 네임스페이스 추가하기
app_name 변수에 네임스페이스 이름을 저장하면 된다.
mysite/pybo/urls.py
```python
from django.urls import path
from . import views

app_name = 'pybo'       # 추가

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
]
```
현재 서버를 실행하면 NoReverseMatch at /pybo/ 오류가 발생한다.
왜냐하면 템플릿에서 아직 네임스페이스를 사용하고 있지 않기 때문이다.
{% url 'detail' question.id %} 을 {% url 'pybo:detail' question.id %} 로 수정한다

## pybo/question_list.html 수정하기
```html
  <ul>
    {% for question in question_list %}
      <li><a href="{%  url 'pybo:detail' question_id %}">{{ question.subject }}</a></li> <!-- 수정 -->
    {% endfor %}
  </ul>
```
detail에 pybo라는 네임스페이스를 붙여준 것이다. 


# 답변 저장하고 표시하기

## 질문 상세 템플릿에 답변 등록 버튼 만들기
templates/pybo/question_detail.html
```html
<h1>{{ question.subject }}</h1>

<div>
  {{ question.content }}
</div>

<!-- 추가 -->
<form action="{% url 'pybo:answer_create' question.id %}" method="post">
  {% csrf_token %}
  <textarea name="content" id="content" rows="15"></textarea>
  <input type="submit" value="답변 등록">
</form>
```
{% csrf_token %} 은 보안관련 항목으로 form 엘리먼트를 통해 전송된 데이터(답변)가 실제로 웹 브라우저에서 작성된 데이터인지 판단하는 검사기 역할을 한다.
그래서 \<form ...> 태그 바로 밑에 {% csrf_token %} 을 항상 입력해야 한다. 해킹처럼 올바르지 않은 방법으로 데이터가 전송되면 서버에서 발행한 csrf_token값과 해커가 보낸 csrf_token 값이 일치하지 않으므로 오류를 발생시켜 보안을 유지할 수 있다.

### cf) csrf_token은 장고의 기본 기능이다.
csrf_token을 사용하려면 장고에 CsrfViewMiddleware라는 미들웨어를 추가해야 한다. 하지만, 이 미들웨어는 장고 프로젝트 생성 시 자동을 config/settings.py 파일의 MIDDLEWARE라는 항목에 추가되므로 직접 입력할 필요는 없다.
```python
# 생략
MIDDLEWARE = [
    # 생략
    'django.middleware.csrf.CsrfViewMiddleware',
    # 생략
] 
# 생략
```

## 질문 상세 페이지에 접속해 보기
pybo/2에 접속하면 'answer_create를 찾을 수 없다'는 오류 화면이 나타난다. 
왜냐하면 form 엘리먼트의 action 속성에 있는 {% url'pybo:answer_create' question.id %} 해당하는 URL 매핑이 없기 때문이다.
```python
from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),        # 추가
]
```

## answer_create 함수 추가하기
pybo/views.py
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone

# 생략
# 추가
def answer_create(request, question_id):
    """pybo 답변 등록"""
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'),
                               create_date = timezone.now())
```
answer_create 함수에 question_id 매개 변수에는 URL 매핑 정보 값이 넘어 온다. 예를 들어 /pybo/answer/create/2가 요청되면 question_id에는 2가 넘어온다.
request 매개 변수에는 pybo/question_detail.html에서 form태그안 textarea에서 입력된 데이터가 파이썬 객체에 담겨온다. 
이 값을 추출하기 위한 코드가 request.POST.get('content')이다. 
그리고 Question 모델을 통해 Answer 모델을 생성하기 위해 question.answer_set.create 를 사용했다.

## 답변 등록 후 상세 화면으로 이동하게 만들기
답변을 생성한 후 상세 페이지로 돌아가려면 redirect 함수를 사용하면 된다.
###### redirect 함수
함수에 전달되는 값을 참고하여 페이지 이동을 수행한다. redirect 첫 번째 인수에는 이동할 페이지의 별칭을 두 번째 인수에는 해당 URL에 전달해야 하는 값을 입력한다.
pybo/views.py
```python
from django.shorcuts import render, get_object_or_404, redirect     # redirect  추가
from .moduls import Question
from django.utils import timezone

# 생략
def answer_create(request, question_id):
    """pybo 답변 등록"""
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'),
                               create_date = timezone.now())
    # 추가
    return redirect('pybo:detail', question_id = question.id)
```

## 등록된 답변 표시하기
pybo/question_detail.html
```html
# 생략
<h5>{{ question.answer_set.count }}개의 답변이 있습니다.</h5>
<div>
  <ul>
  {% for answer in question.answer_set.all %}
    <li>{{ answer.content }}</li>
  {% end for %}  
  </ul>
</div>
# 생략
```

# 웹 페이지에 스타일 시트 적용하

## 설정 파일에 스태틱 디렉터리 위치 추가하기
config/settings.py
```python
# 생략
STATIC_URL = 'static/'
# 추가
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# 생략
```
BASE_DIR / 'static' 은 mysite(프로젝트 루트)/static을 의미

## 스태틱 디렉터리 만들고 스타일시트 작성하기
mysite(프로젝트 루트)에서 static 디렉터리를 생성한다. static 디렉터리 안에 style.css 생성
static/style.css
```css
/* 추가 */
textarea {
  width: 100%;
}

input[type=submit] {
  margin-top: 10px;
}
```

## 질문 상세 템플릿에 스타일 적용하기
템플릿 파일 맨 위에 {% load static %} 태그 삽입, link엘리먼트 href 속성에 {% static 'style.css' %} 추가
templates/pybo/question_detail.html
```html
<!-- 맨 위에 추가 -->
{% load static %}
<link rel="stylesheet" type="text/css" href="{% static 'style.css' %}">
```

# 템플릿을 표준 HTML 구조로 바꾸기

모든 템플릿 파일을 표준 HTML 구조로 변경하면 body 엘리먼트 바깥 부분은 모두 같은 내용으로 중복된다. 그리고 CSS 파일 이름이 변경되거나 새로운 CSS 파일이 추가되면 head 엘리먼트의 내용을 수정하려고 템플릿 파일을 일일이 찾아다녀야 하는 불편함도 있다.
이러한 불편함을 해소하기 위해 장고는 템플릿 상속(extends) 기능을 제공

## 템플릿 파일의 기본 틀 작성하기
templates/base.html 생성
```html
{% load static %}
<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
        content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <link rel="stylesheet" type="text/css" href="{% static 'bootstrap.min.css' %}">
  <link rel="stylesheet" type="text/css" href="{% static 'style.css' %}">
  <title>Hello, pybo</title>
</head>
<body>
<!-- 기본 템플릿 안에 삽입될 내용 Start -->
{% block content %}
{% endblock %}
<!-- 기본 템플릿 안에 삽입될 내용 End -->
</body>
</html>
```
body 엘리먼트에 {% block content %}와 {% endblock %} 템플릿 태그가 있는데 이 부분이 base.html 템플릿 파일을 상속한 파일에서 구현해야 하는 영역이다.

## 질문 목록 템플릿 수정하기
templates/pybo/question_list.html
```html
<!-- 기존 코드 삭제 후 추가 -->
{% extends 'base.html' %}
{% block content %}
<div class="container my-3">
  ... 생략
</div>
{% endblock %}    <!-- 추가 -->
```
question_detail.html도 같은 방법으로 수정


# Model.objects

### Model.objects.all()
queryset 전체를 부른다.
Model.objects.values() 라고도 사용하는 듯

### Model.objects.get()
조건에 해당하는 결과 값 하나만! 불러온다. 

### Model.objects.filter()
조건에 해당하는 결과 불러오고 검색 결과가 2개 이상이 나올 수 있다.

# get_object_or_404
```python
get_object_or_404(Model, pk=pk)
# 이 코드는 아래 코드와 같은 로직이다.
try::
    model = Model.objects.get(pk=pk)
except:
    raise Http404
```
만약 model에서 에러 발생시 Http404에러 발생

# 1. views.py 파일 분리하기
이 방법은 views.py 파일을 분리하고, 나머지 파일을 수정하지 않는 방법이다.  
이 방법이 전체 코드의 변화가 가장 적다.


### views 디렉터리 생성하기
pybo/views 디렉터리 생성

### views.py 파일을 분리해 views 디렉터리에 각각 저장하기
views.py 파일에 정의한 함수를 기능별로 분리하여 views 디렉터리에 아래 표처럼 저장

| 파일명               | 기능    | 함수                                                         |
|-------------------|-------|------------------------------------------------------------|
| base_views.py     | 기본 관리 | index, detail                                              |
| question_views.py | 질문 관리 | question_create, question_modify, question_delete          |
 | answer_views.py   | 답변 관리 | answer_create, answer_modify, answer_delete                |
 | comment_views.py  | 댓글 관리 | comment_create, question, ..., comment_delete_answer(총 6개) |


### views 디렉터리 생성
pybo에 views 디렉터리 생성하고 안에 위에 파일들 생성
pybo/views/base_view.py
```python
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Question


def index(request):
    """ pybo 목록 출력 """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """ pybo 내용 출력 """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
```


pybo/views/question_views.py
```python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


@login_required(login_url='common:login')
def question_create(request):
    """ pybo 질문등록 """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # 추가한 속성 author 적용
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """ pybo 질문수정 """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """ pybo 질문삭제 """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')
```


pybo/views/answer_views.py
```python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """ pybo 답변등록 """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # 추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """ pybo 답변수정 """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """ pybo 답변삭제 """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)
```


pybo/views/comment_views.py
```python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import CommentForm
from ..models import Question, Answer, Comment


@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """pybo 질문 댓글 등록"""
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """pybo 질문 댓글 수정"""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question_id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.question_id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """pybo 질문 댓글 삭제"""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.question_id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question_id)


@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """pybo 답변 댓글 등록"""
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question_id)
    else:
        form = CommentForm()
    context = {'form': form}
    return redirect(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """pybo 답변 댓글 수정"""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question_id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            commnet = form.save(commit=False)
            commnet.author = request.user
            commnet.modify_date = timezone.now()
            commnet.save()
            return redirect('pybo:detail', question_id=comment.answer.question_id)
    else:
        form = CommentForm(instance=comment)
    context = {'form':form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """pybo 답글 댓글 삭제"""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.answer.question_id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)
```


### __init__.py 작성하기
이렇게 views.py 안의 함수들을 나누고, 마지막으로 views 디렉터리 안에 __init__.py를 생성해야 한다.
pybo/views/__init__.py
```python
from .base_views import *
from .question_views import *
from .answer_views import *
from .comment_views import *
```
이렇게 작성한 이후 pubo/views.py를 삭제한다.


#### cf) __init__.py 의 용도
__init__.py 파일은 해당 디렉터리가 패키지의 일부임을 알려주는 역할을 한다. 만약 game, sound, graphic 등 패키지에 포함된 디렉터리에 __init__.py 파일이 없다면 패키지로 인식되지 않는다.  
python3.3 버전부터는 __init__.py 파일이 없어도 패키지로 인식한다(PEP 420). 하지만 하위 버전 호환을 위해 __init__.py 파일을 생성하는 것이 안전한 방법이다.
다음을 따라 해 보자.


1번 방법은 디버깅 시 urls.py파일부터 함수를 찾을 때 urls.py
파일에는 매핑한 함수명만 있으므로 어떤 파일의 함수인지 
알 수 없다는 단점이 존재한다.  
그래서 여러 사람이 함께 하는 프로젝트에서 1번의 방법은 추천하지 않는다.


# 2. 유지보수에 유리한 구조를 만들기

__init__.py 파일을 삭제한다.

### urls.py 파일 수정하기
pybo/urls.py
```python
from django.urls import path
from .views import base_views, question_views, answer_views, comment_views  # 수정

app_name = 'pybo'

urlpatterns = [     # 전체 수정
    # base_views.py
    path('', base_views.index, name='index'),
    path('<int:question_id>/', base_views.detail, name='detail'),

    # question_views.py
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),

    # answer_views.py
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),

    # comment_views.py
    path('comment/create/question/<int:question_id>/', comment_views.comment_create_question,
         name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', comment_views.comment_modify_question,
         name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', comment_views.comment_delete_question,
         name='comment_delete_question'),
    path('comment/create/answer/<int:answer_id>/', comment_views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/', comment_views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/', comment_views.comment_delete_answer, name='comment_delete_answer'),
]
```
모듈명이 표시되도록 URL 매핑 시 views.index을 base_views.index와 같이 변경했다. 모듈명이 있기 때문에 어떤 파일의 어떤 함수인지 명확하게 인지할 수 있다.

### urls.py 파일 수정하기
mysite/urls.py
```python
from django.contrib import admin
from django.urls import path, include
from pybo.views import base_views       # 수정

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index'),       # 수정
]
```

# 페이징

pybo/view.py
```python
from django.core.paginator import Paginator
from django.shortcuts import render

# (... 생략 ...)

def index(request):
    """pybo 목록 출력"""
    # 입력 인자
    page = request.GET.get('page', '1')     # 페이지
    
    # 조회
    question_list = Question.objects.order_by('-create_date')
    
    # 페이징 처리
    paginator = Paginator(question_list, 10)    # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)
```
page = request.GET.get('page', '1')은 GET 방식 요청 URL에서 page값을 가져올 때 사용한다.

GET 방식 요청 URL 예
> localhost:8000/pybo/?page=1

