## 목차
- 프로젝트 세팅
   - [프로젝트 세팅](#프로젝트-세팅)
   - [URL 구조](#URL-구조)
   - [Model](#모델model)
   - [Django Model API](#django-model-api)
   - [모아보기](#감정-일기-모아보기)
   - [상세 페이지](#상세-페이지)
   - [URL 연결하기](#url-연결하기)
   - [디자인 템플릿 입히기](#디자인-템플릿-입히기)
- Form
   - [HTML Form](#HTML-Form)
   - [Django Form](#Django-form)
   - [CSRF 방지](#CSRF-방지)
   - [작성 페이지 만들기](#작성-페이지-만들기)
   - [Django Form Field](#django-form-field)
   - [Model Form 사용하기](#model-form-사용해서-구현)
   - [유효성 검증](#유효성-검증)
   - [Form에 CSS 입히기](#form에-css-입히기)
   - [수정 기능](#수정-기능)
   - [삭제 기능](#삭제-기능)
   - [메인 URL 설정](#메인-url-설정)
- 다양한 상황 처리
   - [데이터가 없는 경우](#데이터가-없는-경우)
   - [seed 데이터 추가 및 유효성 검사](#seed-데이터-추가-및-추가-이후-유효성-검사)
   - [페이지네이션](#페이지네이션pagination-정리하기)
   - [pagination 구현](#pagination-구현)
- Class View
  - [Create View](#createview)
  - [List View](#list-view)
  - [Detail View](#detail-view)
  - [Update View](#update-view)
  - [Delete View](#delete-view-)
  - [Generic View](#generic-view-정리하기)
  - [그 외](#그-외-context-목록)

# 프로젝트 세팅

1. Django 프로젝트 생성은 django-admin을 이용해서 할 수 있습니다.
```zsh
django-admin startproject mindnote  
```

2. App 생성은 Django 프로젝트 디렉토리 안의 manage.py를 이용해서 할 수 있습니다.
```zsh
python manage.py startapp diary
```

3. Django 프로젝트의 시간대 설정은 settings.py의 TIME_ZONE 항목을 통해 할 수 있습니다.
```python
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul' # 이 부분을 수정합니다.

USE_I18N = True

USE_L10N = True

USE_TZ = True
```

4. Django 프로젝트에 사용할 App을 추가할 때는 settings.py의 INSTALLED_APPS 항목을 사용합니다.

```python
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'diary',  # diary 앱을 추가합니다.
]
```


5. Django는 프로젝트를 생성하면 admin, auth, contenttypes, sessions 등의 필요하다고 생각되는 기본 테이블 구조가 만들어지게 되고 이러한 초기 테이블 구조를 반영하기 위한 migration이 필요합니다.
```zsh
python manage.py migrate
```

6. 서버를 실행하고 Django 초기 페이지가 잘 나오는지 확인합니다.

settings.py
```python
ALLOWED_HOSTS = ['*']
```

7. 터미널에서 서버 실행하기
```zsh
python manage.py runserver 0.0.0.0:8000
```

# URL 구조
URL 구조를 미리 생각해두어야 구조적으로 잘 짜여진 프로젝트를 개발할 수 있다.  

1. 아래를 참고해서 mindnote 앱 디렉토리 아래의 urls.py에 ''(빈 문자열) 패턴과 일치하면 diary 앱의 urls를 보도록 작성해 주세요.

mindnote/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('[A]', include('[B]')),
]
```

빈 문자열 패턴과 일치한다는 것은 아무런 패턴이 없는 경우를 말합니다. 그러니까 http://localhost:8000/ 으로 들어왔을 때를 말하는거죠. 이렇게 들어오면 이 이후의 모든 url 처리는 diary의 urls를 보도록 작성하는 과정입니다.

mindnote/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('diary.urls'))
]
```

그럼 이번에는 diary 앱의 urls.py를 작성해 볼까요? 아래처럼 Django의 '우아한' URL 처리 방식을 이용하면 됩니다.  모든 URL 패턴의 끝에는 / 를 붙여서 URL 패턴 형식을 맞춰줍니다.

mindnote/diary/urls.py
```python
from django.urls import path, include
from . import views

urlpatterns = [
    path('diary/', views.page_list),
    path('diafy/info/', views.info),
    path('diary/write/', views.page_create),
    path('diary/page/<int:page_id>/', views.page_detail),
    path('diary/page/<int:page_id>/edit/', views.page_update),
    path('diary/page/<int:page_id>/delete/', views.page_delete),
]
```

우리는 아직 urls.py에서 정의한 여러 뷰들을 정의하지 않았으므로 이 상태로 개발 서버를 실행하면 에러가 나게 되니까 우선 주석 처리합시다.

# 모델(Model)
DateTimeField는 auto_now와 auto_now_add 옵션이 있다.  

auto_now : 포스트가 마지막으로 저장될 때 시간을 자동적으로 해당 필드에 저장한다.  
-> 데이터의 마지막 수정일 
auto_now_add : 포스트가 처음 생성될 때의 시간을 자동적으로 해당 필드에 저장한다.  
-> 데이터의 생성일  

```python
    dt_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
```
이 두가 모두를 true로 생성하면 에러가 발생한다.  


## 모델 필드(Model Field)
Django는 데이터의 타입에 따라 알맞은 필드(Field)를 사용해서 데이터를 다룹니다. 여기서는 우리가 지금까지 사용했던 몇가지 필드 유형과 필드를 정의할 때 사용할 수 있는 옵션들을 정리해 보도록 하겠습니다.

### 필드 유형(Field Types)
아래는 모델을 정의할 때 데이터에 따라 사용할 수 있는 필드 유형으로 우리가 사용했던 필드들과 그외 타입이 비슷한 필드들의 목록입니다. 이 밖에도 다양한 형식의 필드가 있습니다. 아래의 공식문서를 참고하세요. 

| 필드명	                                              | 설명	                                                | 개별속성                                                                       |
|---------------------------------------------------|----------------------------------------------------|----------------------------------------------------------------------------|
| CharField                                         | 	최대 길이가 정해진 문자열 필드                                 | 	max_length (최대 글자수)                                                       |
| TextField	                                        | 최대 길이가 정해지지 않은 문자열 필드	                             | _                                                                          |
| EmailField	                                       | CharField와 같은 문자열 필드지만 입력된 형식이 이메일 형식 인지를 체크하는 필드	 | max_length=254 (기본값)                                                       |
| URLField	                                         | CharField과 같은 문자열 필드지만 입력된 형식이 URL 형식 인지를 체크하는 필드	 | max_length=200 (기본값)                                                       |
| BooleanField	                                     | True, False 값을 갖는 필드	                              | _                                                                          |
| IntegerField	                                     | 정수 형식의 필드	                                         | _                                                                          |
| FloatField	                                       | 부동 소수점 형식의 필드	                                     | _                                                                          |
| DateField	                                        | 날짜 형식의 필드                                          | 	auto_now (수정 될 때 마다 새로운 값으로 갱신) auto_now_add (생성 될 때 값이 입력 되고 추후 변경하지 않음) | 
| TimeField	                                        | 시간 형식의 필드                                          | 	auto_now, auto_now_add                                                    |
| DateTimeField	| 날짜 시간 형식의 필드	| auto_now, auto_now_add                                                     |

### 필드 옵션(Field options)
모델 필드를 정의할 때 작성할 수 있는 몇 가지 옵션 항목 입니다. 모든 필드에 대해 적용할 수 있으며 반드시 필요한 것은 아니고 선택적으로 적용할 수 있습니다. 더 많은 필드 옵션이 궁금하다면 아래의 공식 문서를 참고하세요. 

| 필드 옵션                                  | 	설명	                                          | 기본값   |
|----------------------------------------|-----------------------------------------------|-------|
| null	                                  | True 일 경우 데이터베이스에 빈 값을 저장할 때 NULL을 사용하게 됩니다.	 | False |
| blank                                  | 	True 일 경우 해당 필드를 비워 둘 수 있게 합니다.	             | False |
| default	                               | 필드에 기본값을 지정할 때 사용합니다.	                        | _     |
| editable                               | 	필드의 수정 가능 여부를 설정합니다.	                        | True  |
| help_text	                             | 해당 필드를 입력할 때 보여줄 도움말을 설정합니다.	                 | _     |
| unique	                                | True 일 경우 중복된 값을 입력할 수 없게 합니다.	               | False                                         |
| verbose_name	                          | 사람이 인식하기 좋은 별명을 필드에 설정합니다.	                   |_|
| validators	| 필드의 유효성 검증에 사용할 검증 목록 입니다.	                   |_|


1. 모델 클래스는 models.Model을 상속 받아서 정의할 수 있습니다.
models.py
```python
from django.db import models

# Create your models here.
class Page(models.Model):
    # 모델 필드 정의
```

2. 각각의 필드는 문자열은 models.CharField, 길이 제한 없는 문자열은 models.TextField, 정수형은 models.IntegerField, 날짜형은 models.DateField로 정의하면 됩니다. 이 중에서 날짜형은 데이터를 생성할 때 자동으로 값이 들어가는 auto_now라는 속성이 있었죠? 이번 감정 일기에서는 직접 날짜를 입력하게 만들 것이기 때문에 적어주지 않겠습니다.
```python
from django.db import models

# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    feeling = models.CharField(max_length=80)
    score = models.IntegerField()
    dt_created = models.DateField()
```

3. 모델 클래스를 문자열로 표시하기 위해 사용하는 __str__() 메소드는 아래와 같이 작성합니다.
```python
from django.db import models

# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    feeling = models.CharField(max_length=80)
    score = models.IntegerField()
    dt_created = models.DateField()

    def __str__(self):
        return self.title
```

4. 이렇게 작성된 모델을 Django가 제공하는 관리자 페이지에서 사용하기 위해서는 admin.py에 등록해 주어야 합니다. 먼저 작성한 모델을 import하고 admin.site.register()를 이용해 등록합니다.
```python
from django.contrib import admin
from .models import Page

# Register your models here.
admin.site.register(Page)
```

작성한 모델을 데이터 베이스에 반영하기 위해서는 먼저 마이그레이션을 만들고 반영하면 됩니다.
```zsh
python manage.py makemigrations
python manage.py migrate
```

# Django Model API
Django에서 Model을 정의하면 ORM을 통해 데이터베이스와 소통할 수 있는 API를 제공합니다. 여기서는 우리가 사용하는 Model API를 정리하고 조금 더 자세히 살펴보겠습니다.

## API란?
우리가 앞에서 데이터베이스를 조작할 때 사용했던 아래와 같은 모든 명령어들이 바로 API 입니다.  
```python
<model>.objects.all() # 모든 데이터 가져오기
<model>.objects.get() # 조건에 맞는 데이터 1개 가져오기
```

API란 Application Programming Interface의 약자로 어플리케이션에서 시스템의 기능을 제어할 수 있도록 만든 인터페이스를 말합니다. 쉽게 말하면 어떤 기능을 쉽게 사용할 수 있도록 만든 체계라고 할 수 있는데요, 예를 들어 여러분이 식당에 가면 주문을 받는 직원이 있죠? 우리는 해당 직원을 통해서 먹고 싶은 음식을 주문하고 전달 받아서 맛있게 먹으면 됩니다. 직접 요리사에게 먹고 싶은 음식에 대해 설명하거나 만드는 법을 알려줄 필요가 없죠. 여기서 직원에 해당하는 것이 바로 API 입니다.  

## Queryset
Queryset은 Django Model의 데이터가 담겨있는 목록으로 파이썬의 리스트와 비슷한 형태를 가지고 있습니다. 우리는 이러한 Queryset을 얻기 위해서 아래와 같은 'objects'를 이용합니다. 이 'objects'는 'Model Manager'라고 하는데 Model과 데이터베이스 간에 연산을 수행하는 역할을 합니다. 이 'objects'를 통해 데이터베이스와 연산해서 얻은 여러 모델 데이터가 담겨 있는 것이 바로 Queryset 인거죠.  
```zsh
<model>.objects.all() # <model>의 모든 데이터 Queryset 가져오기 
```

### Queryset API
자, 어려운 내용은 잠시 내려두고 쉽게 말해서 Queryset은 데이터베이스로 부터 가져온 여러개의 model 데이터 입니다. 우리는 이러한 Queryset을 우리가 원하는 조건에 맞게 만들 수 있으면 되는거죠.  

#### Queryset을 반환 하는 API
| API	                                                                             | 설명 |	예시  |
|----------------------------------------------------------------------------------|----|----|
| all()	                                                                           | 해당 모델 테이블의 모든 데이터 조회|	Post.objects.all() |
| filter()	|특정 조건에 맞는 모든 데이터 조회	|Post.objects.filter(content__contains='coke')      |
| exclude()|	특정 조건을 제외한 모든 데이터 조회	|Post.objects.exclude(title__contains='code')      |
| order_by()|	특정 조건으로 정렬된 데이터 조회                                                 (-를 붙이면 오름차순으로 정렬)|	Post.objects.order_by('-dt_created')                          |
| values()|	Queryset에 있는 모든 모델 데이터의 정보를 사전형으로 갖는 리스트 반환	|Post.objects.all().values() |


#### 하나의 데이터 객체를 반환하는 API
| API	                                                                             | 설명 |	예시  |
|----------------------------------------------------------------------------------|----|----|
|get()|	조건에 맞는 하나의 데이터 조회|	Post.objects.get(id=1) |
|create()|	하나의 데이터를 생성하고 해당 모델 데이터를 반환|	Post.objects.create(title='Learning Django', context='Codeit Django')|
|get_or_create()|	조건에 맞는 데이터를 조회하고 해당 데이터가 없다면 새로 생성 후 생성된 모델 데이터를 반환|	Post.objects.get_or_create(title='Learning Python', context='It's good’)|
|latest()|	주어진 필드 기준으로 가장 최신의 모델 데이터를 반환|	Post.objects.latest('dt_created')|
|first()|	쿼리셋의 가장 첫번째 모델 데이터를 반환, 정렬하지 않은 쿼리셋이라면 pk를 기준으로 정렬 후 반환, 만약 데이터가 없다면 None|	Post.objects.order_by('title').first()|
|last()|	연산된 쿼리셋의 가장 가지막 모델 데이터를 반환, 만약 데이터가 없다면 None	|Post.objects.order_by('title').last()|

#### 그 외 API
| API	                                                                             | 설명 |	예시  |
|----------------------------------------------------------------------------------|----|----|
|exists()	|연산된 쿼리셋에 데이터가 있다면 True 반환	|Post.objects.get(pk=812).exists() |
|count()	|쿼리셋의 데이터 개수를 정수로 반환	|Post.objects.all().count()|
|update()	|데이터를 수정할 때 사용(여러 데이터 또는 여러 필드를 한 번에 수정 가능), 수정된 데이터의 개수를 정수로 반환|	Post.objects.filter(dt_created__year=2021).update(context='codeit') → 생성일이 2021년인 모든 포스트 데이터들의 context를 'codeit'으로 바꾸고 변경된 데이터의 개수를 리턴|
|delete()	|데이터를 삭제할 때 사용|	post = Post.objects.get(pk=1) post.delete()|

### 필드 조건 옵션 (Field Lookups)  
Queryset 연산을 할 때 사용할 수 있는 여러 필드 조건 옵션입니다. 필드명 뒤에 __ 를 쓰고 사용할 옵션 인자를 적어 주면 됩니다. 아래의 조건 옵션 말고도 더 많은 옵션 들이 있습니다. 아래의 공식 문서를 참고하세요.  

| lookup	                                                                                                                                                                                                     |설명	|예시|
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|----|
| __contains|	대소문자를 구분하여 문자열 포함 여부 확인|	Post.objects.get(title__contains='Codeit')                                                                                                                               |
| __icontains	|대소문자를 구분하여 문자열 불포함 여부 확인|	Post.objects.get(title__icontains='Codeit')                                                                                                                            |
| __in	|반복 가능한 객체 안에서의 포함 여부를 확인|	Post.objects.filter(id__in=[1, 2, 3])                                                                                                                                         |
| __gt|	초과 여부 확인 (Greater than)|	Post.objects.filter(id__gt=4)                                                                                                                                                  |
| __gte|	이상 여부 확인 (Greater than or equal to)|	Post.objects.get(id__gte=4)                                                                                                                                       |
| __lt|	미만 여부 확인 (Less than)	|Post.objects.get(id__lt=4)                                                                                                                                                        |
| __lte|	이하 여부 확인 (Less than or equal to)|	Post.objects.get(id__lte=4)                                                                                                                                          |
| __startswith|	대소문자를 구분하여 해당 문자열로 시작하는지 여부 확인|	Post.objects.filter(title__startswith='code')                                                                                                                   |
| __istatswith|	대소문자를 구분하여 해당 문자열로 시작하지 않는지 여부 확인|	Post.objects.filter(context__istartswith='code')                                                                                                             |
| __endswith	|대소문자를 구분하여 해당 문자열로 끝나는지 여부 확인|	Post.objects.filter(title__endswith='code')                                                                                                                        |
| __iendswith|	대소문자를 구분하여 해당 문자열로 끝나지 않는지 여부 확인|	Post.objects.filter(title_iendswith='code')                                                                                                                    |
| __range	|range로 제시하는 범위 내에 포함되는지 확인(시작과 끝 범위 모두 포함)|	import datetime start_date = datetime.date(2021, 1, 1) end_date = datetime.date(2021, 3, 1) Post.objects.filter(dt_created__range=(start_date, end_date)) |
| __isnull|	해당 필드가 Null 인지 여부를 확인|	Post.objects.filter(context__isnull=True)                                                                                                                                    |

### Lazy Evaluation (지연연산)
위에서 작성한 Django의 모든 Query 연산은 병합(Chain)이 가능합니다. 예를들어, Post 중에 id가 10 이상이면서 제목에 'codeit'이 들어가는 모든 데이터 중 가장 마지막에 작성된 데이터를 가져오고 싶다고 할게요. 그러면 아래 처럼 작성할 수 있습니다.  
```zsh
Post.objects.filter(id__gte=10, content__contains='codeit').order_by('-dt_created').last()
```
이렇게 하나의 Query 연산에 여러개를 체인으로 엮어서 구현하는 것이 코드를 짧게 작성하니까 좋다고 생각할 수 있지만 너무 많은 연산을 묶는 것은 지양해야 합니다. 모든 코드는 항상 명확하게 작성해야 합니다. 위처럼 하나의 Query에서 여러 연산을 수행 하도록 하는 것은 가독성을 매우 떨어뜨리므로 복잡한 Query를 한 번에 체인으로 묶는 것은 피하는 것이 좋습니다. 대신 아래처럼 작성하는 거죠. 이전보다 이해하기 쉽고 명확한 코드가 되었습니다.  
```zsh
post_data = Post.objects.filter(id__gte=10, content__contains='codeit')
post_data = post_data.order_by('dt_created')
post_data = post_data.last()
```
그런데 이렇게 여러 번에 나누어서 작성하면 코드가 훨씬 느려지는 것은 아닐까요? 그에 대한 답은 '그렇지 않다' 입니다. Django의 Query는 기본적으로 지연 연산을 지원합니다. 지연 연산이란 실제로 데이터가 필요하기 전 까지 Query 연산을 수행하지 않고 지연(Lazy)되는 것을 말합니다. 우리가 위에서 처럼 모두 체인으로 묶어서 한 줄로 적는 것과 아래처럼 여러 줄로 나누어 적는 것이 결국 같은 시점에 같은 연산을 수행하게 되는 것이죠. 그래서 우리는 한 줄에 모든 Query 연산과 기능을 작성 하는 것 대신 여러 줄에 얼마든지 Query를 연결해서 작성할 수 있고, 이것은 가독성을 엄청나게 크게 향상시키고 유지보수를 편리하게 해줍니다.

# 감정 일기 모아보기

1. 관리자 계정은 manage.py를 이용해서 생성할 수 있습니다.  

터미널
```zsh
python manage.py createsuperuser
```

2. diary/templates/diary 디렉토리 구조안에 page_list.html을 간단한 <h2> 태그로 생성합니다.

page_list.html
```html
<h2>일기 목록 페이지</h2>
```

3. urls.py로 가서 page_list뷰로 연결된 패턴을 주석 해제 하고 page_list뷰를 정의합니다.

urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('diary/', views.page_list),
    # path('diafy/info/', views.info),
    # path('diary/write/', views.page_create),
    # path('diary/page/<int:page_id>/', views.page_detail),
    # path('diary/page/<int:page_id>/edit/', views.page_update),
    # path('diary/page/<int:page_id>/delete/', views.page_delete),
]
```

먼저 사용할 Page 모델을 가져온 다음, 모든 데이터를 조회한 후 page_list 템플릿으로 넘겨 줍니다. 

views.py
```python
from django.shortcuts import render
from .models import Page

# Create your views here.
def page_list(request):
    return render(request, 'diary/page_list.html')
```

4. 개발 서버를 켜고 page_list 템플릿이 잘 나오는지 확인합니다.

5. Page 모델을 이용해서 데이터베이스로 부터 모든 데이터를 조회 한 후 page_list 템플릿으로 전달합니다. 이때 object_list를 키로 사용합니다.  

views.py
```python
from django.shortcuts import render
from .models import Page

# Create your views here.
def page_list(request):
    object_list = Page.objects.all() # 데이터 조회
    return render(request, 'diary/page_list.html', {'object_list': object_list})
```

6. 이제 page_list 템플릿으로 가서 전달받은 데이터를 이용해 모든 데이터를 표시하게끔 작성하면 됩니다. 먼저 글이 반복되는 부분을 확인하고 {for} 템플릿 태그를 이용해서 반복하게끔 작성합니다.

page_list.html
```html
<h2>일기 목록 페이지</h2>

<ul>
        {% for obj in object_list %}
        <!-- 하나의 글은 여기서부터 -->
    <li>
        <div class="date">
            <span><!--날짜 중 '일'--></span>
                        <p><!--날짜 중 '월'--></p>
        </div>
        <h2><!--제목--></h2>
        <div class="score">
            <p>감정점수</p>
            <span><!--감정점수-->점</span>
        </div>
    </li>
        <!-- 여기까지 반복됩니다. -->
        {% endfor %}
</ul>
```
그다음 뷰에서 전달받은 데이터를 표시하도록 템플릿 변수를 이용해 작성합니다. 그중 '일'과 '월'에 해당하는 부분은 템플릿 필터를 이용해서 해당 데이터만 보여 주도록 처리합니다.
```html
<h2>일기 목록 페이지</h2>

<ul>
    {% for obj in object_list %}
    <li>
        <div class="date">
            <span>{{obj.dt_created|date:"d"}}</span>
            <p>{{obj.dt_created|date:"M"}}</p>
        </div>
        <h2>{{obj.title}}</h2>
        <div class="score">
            <p>감정점수</p>
            <span>{{obj.score}}점</span>
        </div>
    </li>
    {% endfor %}
</ul>
```

7. 개발 서버를 켜고 /diary/로 들어가서 목록 페이지가 잘 나오는지 확인합니다.

# 상세 페이지

1. 먼저 urls.py로 가서 상세 페이지에 대한 주석을 해제합니다.
urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('diary/', views.page_list),
    # path('diafy/info/', views.info),
    # path('diary/write/', views.page_create),
    path('diary/page/<int:page_id>/', views.page_detail),
    # path('diary/page/<int:page_id>/edit/', views.page_update),
    # path('diary/page/<int:page_id>/delete/', views.page_delete),
]
```

2. page_detail뷰를 정의하는데, 이때 urls에서 넘겨주는 page_id를 파라미터로 받습니다. 그리고 이 page_id를 이용해서 해당 Page 데이터를 조회하고 템플릿으로 전달 합니다.  
views.py
```python
def page_detail(request, page_id):
    object = Page.objects.get(id=page_id)
    return render(request, 'diary/page_detail.html', {'object': object})
```

3. diary/templates/diary/page_detail.html을 작성합니다. 뷰에서 넘겨준 데이터를 이용해서 템플릿 변수로 각각 데이터가 표시될 부분을 작성하면 됩니다.

page_detail.html

```html
<div class="notetext">
    <div class="text-box">
        <h2>{{object.title}}</h2>
        <div class="state">
            <p>감정 상태</p>
            <span>{{object.feeling}}</span>
        </div>
        <div class="score">
            <p>감정 점수</p>
            <span>{{object.score}}점</span>
        </div> 
        <div class="date">
            <span>{{object.dt_created|date:"d"}}</span>
            <div class="month-year">
                <p class="month">{{object.dt_created|date:"M"}}</p>
                <p class="year">{{object.dt_created|date:"Y"}}</p>
            </div>
        </div>
        <div class="detail">{{object.content}}</div>
        <div class="notetext-btn">
            <ul>
                <li><a href="#">삭제하기</a></li>
                <li><a href="#">수정하기</a></li>
            </ul>
        </div>
    </div>
</div>
```

4. 일기 내용이 표시되는 {{ object.content }}에는 줄 바꿈을 <br> 태그로 바꿔주는 linebreaksbr 템플릿 필터를 적용합니다.

```html
<div class="notetext">
    ...
        <div class="detail">{{object.content|linebreaksbr}}</div>
    ...
</div>
```

5. page_list 템플릿으로 가서 이제 각각의 일기를 눌렀을 때 상세 글로 이동하도록 작성합니다. \<a> 태그를 이용하면 됩니다. 우리는 하나의 글 전체를 클릭할 수 있는 링크로 만들어 주겠습니다. 클릭했을 때 이동할 URL은 기존의 각 데이터의 id를 포함 해야 합니다. 앞에서 urls.py에 상세 글로 가는 url 패턴을 /diary/page/<int:page_id> 형식으로 작성했기 때문입니다.  
조금 더 설명을 하자면 page_detail 뷰에서 object_list로 모든 데이터를 넘겨 주었고, 우리는 object_list에서 하나씩 Page 데이터를 꺼내서 반복을 하고 있으므로 이 반복 인자인 obj를 이용하면 하나의 Page 데이터에 대한 id 값에 접근할 수 있는거죠.

page_list.html

```html
<h2>일기 목록 페이지</h2>

<ul>
    {% for obj in object_list %}
    <li>
        <a href="/diary/page/{{obj.id}}">
            <div class="date">
                <span>{{obj.dt_created|date:"d"}}</span>
                <p>{{obj.dt_created|date:"M"}}</p>
            </div>
            <h2>{{obj.title}}</h2>
            <div class="score">
                <p>감정점수</p>
                <span>{{obj.score}}점</span>
            </div>
        </a>
    </li>
    {% endfor %}
</ul>
```
6. 개발 서버를 켜고 /diary/로 이동한 후 각각의 일기 글을 눌러서 상세 보기로 잘 이동하는지 확인합니다.


# URL 연결하기
1. urls.py로 가서 모든 url에 name을 지정해 줍니다.

```python
from django.urls import path
from . import views

urlpatterns = [
    path('diary/', views.page_list, name='page-list'),
    # path('diary/info/', views.info, name='info'),
    # path('diary/write/', views.page_create, name='page-create'),
    path('diary/page/<int:page_id>/', views.page_detail, name='page-detail'),
    # path('diary/page/<int:page_id>/edit/', views.page_update, name='page-update'),
    # path('diary/page/<int:page_id>/delete/', views.page_delete, name='page-delete'),
]
```

2. page_list 템플릿으로 가서 하드코딩 되어있는 형태 대신 {url} 템플릿 태그를 이용하도록 수정합니다. 이때 상세 보기 페이지는 id값이 url에 필요하므로 함께 넘겨줄 수 있습니다.
```html
<h2>일기 목록 페이지</h2>

<ul>
    {% for obj in object_list %}
    <li>
        <a href="{% url 'page-detail' obj.id %}">
            ...
    {% endfor %}
</ul>
```

# 디자인 템플릿 입히기

1. 모든 템플릿의 부모 템플릿이 될 base 템플릿을 작성하는 과정입니다. 먼저 [A]에는 정적 파일 경로를 사용하기 위한 {load static} 템플릿 태그를 작성합니다.

base.html
```html
{% load static %} <!-- [A]- 정적 파일 로드 -->
<!DOCTYPE html>
<html lang="en">
 ...
</html>
```

[B]는 styles.css의 경로를 적어 주면 되는데 {static} 템플릿 태그를 이용합니다.  
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Mind Note</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="{% static 'diary/css/styles.css' %}">
        <link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/moonspam/NanumSquare/master/nanumsquare.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_two@1.0/NanumBarunpen.woff">
    </head>
    ...
</html>
```

[C]~[E]는 모두 {url} 템플릿 태그를 이용해서 이동할 링크를 적어 주면 됩니다. 이때 url을 직접 하드 코딩 하지 않고 url-name을 사용하는 것이 좋습니다.
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Mind Note</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="{% static 'diary/css/styles.css' %}">
        <link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/moonspam/NanumSquare/master/nanumsquare.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_two@1.0/NanumBarunpen.woff">
    </head>
    <body>
        <div class="menu">
            <h1><a href="{% url 'page-list' %}"><img src="{% static 'diary/image/logo02.svg' %}"></a></h1>
            <ul>
                <li><a href="{% url 'page-list' %}">모아보기</a></li>
                <li><a href="{% url 'info' %}">감정일기란</a></li>
                <li><a href="#">일기쓰기</a></li>
            </ul>
        </div>

        {% block content %}
        {% endblock content %}

    </body>
</html>
```

2. page_list 템플릿에 먼저 base 템플릿을 상속 받도록 {extend} 템플릿 태그를 사용해서 구현합니다.  

page_list.html
```html
<!-- content block 처리 -->
{% extends './base.html' %}

<!-- content 블럭 처리 -->
<div class="wrap-note">
    <div class="note">         
        <div class="note-list">
            <ul>
                {% for obj in object_list %}
                <li>
                    <a href="{% url 'page-detail' obj.id %}">
                        <div class="date">
                            <span>{{obj.dt_created}}</span>
                        </div>
                        <h2>{{obj.title}}</h2>
                        <div class="score">
                            <p>감정점수</p>
                            <span>{{obj.score}}점</span>
                        </div>
                    </a>
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
<!-- content 블럭 처리 -->
```

그 다음 {block}을 이용해서 템플릿을 구현합니다. {block}은 block의 끝을 명시해 주어야 하므로 {endblock} 태그와 쌍을 이룹니다.  

page_list.html
```html
{% extends './base.html' %}

{% block content %} <!-- content block 처리 -->
<div class="wrap-note">
    <div class="note">         
        <div class="note-list">
            <ul>
                {% for obj in object_list %}
                <li>
                    <a href="{% url 'page-detail' obj.id %}">
                        <div class="date">
                            <span>{{obj.dt_created|date:"d"}}</span>
                            <p>{{obj.dt_created|date:"M"}}</p>
                        </div>
                        <h2>{{obj.title}}</h2>
                        <div class="score">
                            <p>감정점수</p>
                            <span>{{obj.score}}점</span>
                        </div>
                    </a>
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
{% endblock content %} <!-- content block 처리 -->
```

3. page_detail 역시 base 템플릿 상속과 content 블럭 처리를 해줍니다.

page_detail.html
```html
{% extends './base.html' %} <!-- base 템플릿 상속 -->

{% block content %} <!-- content block 처리 -->
<div class="wrap-notetext">
    <div class="notetext">
        <div class="text-box">
            <h2>{{object.title}}</h2>
            <div class="state">
                <p>감정 상태</p>
                <span>{{object.feeling}}</span>
            </div>
            <div class="score">
                <p>감정 점수</p>
                <span>{{object.score}}점</span>
            </div> 
            <div class="date">
                <span>{{object.dt_created|date:"d"}}</span>
                <div class="month-year">
                    <p class="month">{{object.dt_created|date:"M"}}</p>
                    <p class="year">{{object.dt_created|date:"Y"}}</p>
                </div>
            </div>
            <div class="detail">{{object.content|linebreaksbr}}</div>
            <div class="notetext-btn">
                <ul>
                    <li><a href="#">삭제하기</a></li>
                    <li><a href="#">수정하기</a></li>
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock content %} <!-- content block 처리 -->
```

4. 일기 소개 페이지를 만들어 봅시다. 템플릿부터 작성해 볼게요. info.html을 열고 마찬가지로 base 템플릿을 상속받고 안에 내용 부분을 content 블럭으로 처리해 주겠습니다.

info.html
```html
{% extends './base.html' %} <!-- base 템플릿 상속 -->

{% block content %} <!-- content 블럭 처리 -->
<div class="wrap-mindnote">
    <div class="mindnote">
        <ul>
            ...
        </ul>
    </div>
</div>
{% endblock content %} <!-- content 블럭 처리 -->
```

그 다음 urls.py로 가서 소개에 대한 url을 주석 해제해 주겠습니다.
```python
from django.urls import path
from . import views

urlpatterns = [
    path('diary/', views.page_list, name='page-list'),
    path('diary/info/', views.info, name='info'), # 주석 해제
    # path('diary/write/', views.page_create, name='page-create'),
    path('diary/page/<int:page_id>/', views.page_detail, name='page-detail'),
    # path('diary/page/<int:page_id>/edit/', views.page_update, name='page-update'),
    # path('diary/page/<int:page_id>/delete/', views.page_delete, name='page-delete'),
]
```

그리고 마지막으로 views.py 로 가서 info뷰를 작성합니다. info뷰는 간단하게 info 템플릿을 렌더해서 결과로 돌려주도록 작성하면 됩니다.  

views.py
```python
from django.shortcuts import render
from .models import Page

...

def info(request):
    return render(request, 'diary/info.html')

...
```

# HTML Form
폼은 웹 페이지에서 사용자의 데이터를 입력받을 수 있는 입력 양식을 말합니다.  아래에서 배우는 여러 Form 요소들은 Django에서 제공하는 폼을 사용하면 저절로 생성되지만 기본적인 HTML 폼을 알고 있으면 Django의 폼을 이해하는데 많은 도움이 됩니다.  

### label과 input
폼은 form태그 안에 사용자의 입력을 받는 input태그와 설명을 위한 label태그의 쌍으로 구성됩니다.  
```html
<form>
    <lable>이름</lable>
    <input type="text">
</form>
```

### for & id
각각의 input태그와 label태그를 묶어주기 위해서 label태그에는 for 속성, input태그에는 id가 사용됩니다.  
```html
<form>
    <label for="title">제목</label>
    <input type="text" id="title">
</form>
```

만약 여기에서 for와 id 속성을 적어주고 싶지 않다면 label 태그로 input태그를 감싼 형태를 사용하면 됩니다.  
```html
<form>
    <label>제목
        <input type="text">
    </label>
</form>
```

### name
name은 입력된 데이터를 서버로 전송할 때, 서버에서 각각의 데이터를 구분하기 위한 속성으로 name 속성이 있는 양식 요소만 값이 서버로 전달됩니다.
```html
<form>
    <label for="title">제목</label>
    <input type="text" id="title" name="title">
</form>
```

### type
type은 입력할 값에 따른 유형을 나타내는 속성입니다. 이 type에 따라 사용자가 브라우저에서 값을 입력하는 형식인 위젯(widget)이 달라집니다. 자주 사용되는 type은 아래와 같습니다.
- email
```html
<label for="email">이메일</label>
<input type="email" id="email" name="email">
```

- password
```html
<label for="pwd">비밀번호</label>
<input type="password" id="pwd" name="pwd">
```

- button
```html
<input type="button" value="버튼입니다">
```

- radio
```html
<input type="radio" id="male" name="gender" value="male">
<label for="male">남자</label><br>
<input type="radio" id="female" name="gender" value="female">
<label for="female">여자</label><br>
<input type="radio" id="other" name="gender" value="other">
<label for="other">기타</label>
```
checkbox
```html
<input type="checkbox" id="lang1" name="lang1" value="Python">
<label for="lang1">파이썬(Python)</label><br>
<input type="checkbox" id="lang2" name="lang2" value="JAVA">
<label for="lang2">자바(JAVA)</label><br>
<input type="checkbox" id="lang3" name="lang3" value="Go">
<label for="lang3">고(Go)</label><br>
```

- date
```html
<label for="birthday">생년월일</label>
<input type="date" id="birthday" name="birthday">
```

- file
```html
<label for="userfiles">파일선택</label>
<input type="file" id="userfiles" name="userfiles" multiple>
```

- submit
```html
<input type="submit" value="전송하기"> 
```

### form 속성
form에는 입력된 데이터를 전송할 서버의 URL을 지정하는 action과 http 전달 방식을 지정해 주는 method 속성이 있습니다.
```html
<form action="register" method="post">
    <label for="name">이름</label>
    <input type="text" id="name" name="name">
    <input type="submit" value="제출하기">
</form>
```

### GET과 POST
GET 방식으로 지정하면 유저가 데이터를 입력하고 전송했을 때 URL 뒤에 쿼리 스트링(Query String) 형태로 데이터가 전달됩니다.

```html
<form action="/register" method="get">
    <label for="name">이름</label>
    <input type="text" id="name" name="name">
    <label for="email">이메일</label>
    <input type="email" id="email" name="email">
    <input type="submit" value="제출하기">
</form>
```

> http://www.codeit-django.com/register?name=우재&email=woojae@codeit.kr


POST 방식은 전송되는 URL에는 표시되지 않고 서버로 전송하는 메세지 안쪽에 데이터를 넣어서 전달합니다. 이 부분에 대해서는 조금 더 나중에 자세하게 다루겠습니다.

```html
<form action="/register" method="post">
    <label for="name">이름</label>
    <input type="text" id="name" name="name">
    <label for="email">이메일</label>
    <input type="email" id="email" name="email">
    <input type="submit" value="제출하기">
</form>
```

> http://www.codeit-django.com/register

그러면 언제 GET을 사용하고 언제 POST를 사용해야 할까요? 그것을 결정하는 것은 이 요청이 무엇을 하는지에 달려 있습니다. GET은 가져오다는 의미처럼 서버에서 데이터를 가져오는 요청을 보낼 때 사용하고 그 외에 서버의 데이터를 변경하거나 다른 로직을 수행할 때는 POST를 사용합니다. 간단히 정리하면 form을 사용할 때는 사용자로부터 데이터를 입력받아서 저장, 수정 등의 데이터베이스와 관련된 로직을 많이 수행하죠? 그렇기 때문에 form에서는 대부분의 경우 POST를 사용한다고 생각하면 됩니다.


# Django form
1. diary/forms.py 안에 PageForm 클래스를 작성합니다. Form 클래스는 Django의 forms.Form을 상속하고 각각의 폼 필드를 작성하면 됩니다. 이때 content 같은 경우 여러줄 입력이 가능한 Textarea 위젯을 파라미터로 넘겨주어 위젯을 명시해 줍니다. 명시하지 않은 다른 폼 필드들은 각 필드 타입에 따른 기본 위젯으로 설정 됩니다.

```python
from django import forms

class PageForm(forms.Form):
    title = forms.CharField(max_length=100, label='제목')
    content = forms.CharField(widget=forms.Textarea, label='내용')
    feeling = forms.CharField(max_length=80, label='감정 상태')
    score = forms.IntegerField(label='감정 점수')
    dt_created = forms.DateField(label='작성일')
```

2. urls.py로 가서 일기 작성에 해당 하는 URL의 주석을 해제 합니다.
```python
from django.urls import path
from . import views

urlpatterns = [
    path('diary/', views.page_list, name='page-list'),
    path('diary/info/', views.info, name='info'),
    path('diary/write/', views.page_create, name='page-create'), # 주석 해제
    path('diary/page/<int:page_id>/', views.page_detail, name='page-detail'),
    # path('diary/page/<int:page_id>/edit/', views.page_update, name='page-update'),
    # path('diary/page/<int:page_id>/delete/', views.page_delete, name='page-delete'),
]
```

3. 이제 views.py로 가서 page_create뷰를 작성하면 됩니다. page_create뷰는 page_form 템플릿을 렌더해서 결과로 돌려 주는데, 이때 작성했던 PageForm을 page_form 템플릿으로 함께 넘겨주도록 작성하면 됩니다.
```python
from django.shortcuts import render
from .models import Page
from .forms import PageForm

... 

def page_create(request):
    form = PageForm()
    return render(request, 'diary/page_form.html', {'form': form})

...
```

4. 그리고 아직 page_form 템플릿을 작성한 적이 없죠? page_form 템플릿을 작성합니다. 보면 미리 {form} 태그와 작성하기 버튼이 작성되어 있는데 여기에 page_create뷰에서 넘겨준 form을 이용해서 작성합니다. 각각의 입력 요소들을 <p> 태그로 렌더해주는 as_p를 사용하겠습니다.
```html
<form method="post">
    {{form.as_p}}
    <input type="submit" value="작성하기">
</form>
```

이렇게 작성하면 forms.py에서 작성한 대로 각각의 폼 필드에 알맞은 형태로 html 태그가 생성됩니다.

5. 마지막으로 base.html로 가서 '일기 쓰기'로 이동하는 링크에 지금 작성한 page-create를 연결해 주면 됩니다. {url} 템플릿 태그를 이용하면 되겠죠?
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
...
<body>
    <div class="menu">
        <h1><a href="{% url 'page-list' %}"><img src="{% static 'diary/image/logo02.svg' %}"></a></h1>
        <ul>
            <li><a href="{% url 'page-list' %}">모아보기</a></li>
            <li><a href="{% url 'info' %}">감정일기란</a></li>
            <li><a href="{% url 'page-create' %}">일기쓰기</a></li>
        </ul>
    </div>
    {% block content %}
    {% endblock content %}
</body>
```

6. 다 되었습니다. 개발 서버를 켜고 /diary/로 이동해서 '일기 쓰기'를 눌러 일기 작성 폼이 잘 나오는지 확인합니다. 아직 폼이 입력은 되지만 동작은 하지 않습니다. 이 부분은 다음 실습에서 작성해 보도록 할게요.


# CSRF 방지
크로스 사이트 요청 위조(CSRF, Cross-Site Request Forgery)는 간단히 말하면 웹 사이트에서 유저가 서버로 요청을 보내는 행위를 악의적으로 변경해서 요청을 전송하는 것입니다. 내가 요청하지 않은 일인데 내가 요청한 것처럼 처리되는 거죠.  

### 크로스 사이트 요청 위조
Cross-Site라는 말이 붙은 이유는 악성 사이트에서 보안이 취약한 사이트로 우회 요청을 보내기 때문인데요. 예를들면 다음과 같은 단계로 요청 위조가 일어날 수 있습니다.

1. 유저가 보안이 취약한 사이트(www.example-weak.com)에 로그인을 합니다. 아이디와 패스워드등의 유저 입력을 받아서 서버로 전송해야 하니까 폼(Form)을 사용하겠죠?
2. 서버가 유저가 전송한 정보를 보고 이 유저가 정상유저임을 인증합니다. 로그인이 성공한 상태죠. 이때 보이지 않지만 서버로부터 인증된 유저라는 정보가 유저에게도 전달되게 됩니다. 이 정보를 사용해서 서버는 매번 로그인을 요청 하지 않고도 이 유저가 로그인 한 유저라는 것을 식별하는거죠.
3. 이 상태에서 유저가 로그아웃 하지 않은 채, 악성 사이트(www.example-malicious.com)로 이동합니다. 우리가 웹 서핑을 할 때 흔히 하는 동작이죠.
4. 그러면 이제 악성 사이트에서 다음과 같은 유저의 정보를 가져오거나, 돈을 송금하는 등의 요청을 전송하는 폼을 누르게 하거나 해당 폼을 굳이 작성하지 않아도 자동으로 전송 되는 형태로 요청을 시도합니다. action을 보면 지금 악성 사이트에서 취약한 사이트로 요청을 보내고 있죠? 크로스 사이트 요청이 일어나는 부분입니다.
```html
<form action="www.example-weak.com/user-info/account" method="post">
    <div>응모에 당첨되셨습니다!</div>
    <label type="hidden" name="withdraw" value="withdraw"> # 숨김 처리된 input
    <label type="hidden" name="amount" value="1000000">  # 숨김 처리된 input
    <input type="submit" value="경품받기">
</form>
```

5. 요청을 보낼 때 유저가 가지고 있는 인증 정보도 함께 서버로 전송됩니다.
6. 취약한 사이트에서는 인증된 유저가 보낸 요청이므로 요청을 수행하게 됩니다.

### 위조 방지 토큰
위에서 보았던 크로스 사이트 요청 위조를 방지하는 방법으로 많이 사용하는 것이 바로 CSRF 위조 방지 토큰(Cross Site Request Forgery Token)입니다. 요청 위조 방지 토큰은 서버로부터 폼을 요청할 때 발행되어 유저가 폼에 데이터를 입력하고 서버로 전송할 때 이 토큰 값을 함께 전달해서 서버에서 토큰 값을 비교한 뒤 요청을 처리하는 방식을 말합니다. 그래서 요청 검증 토큰(Request Verification Token)라고 부르기도 합니다. 이렇게 처리하면 위의 예시에서 악성 사이트가 폼을 전송할 때 이 위조 방지 토큰 값을 알 수 없기 때문에 서버에서 사용자가 직접 보낸 요청인지를 검증할 수 있게 되는 거죠.

### Django의 CSRF 방지
Django는 CSRF 위조 방지를 기본 기능으로 제공해서 위조 방지 토큰을 삽입하고 검증하는 과정을 간단하게 구현할  수 있습니다. 폼을 사용하는 템플릿에 아래 처럼 {% csrf_token %} 템플릿 태그를 적어 주면 됩니다.
```html
<form action="/user" method="post">{% csrf_token %}
    ...
</form>
```

이 밖에도 다양한 외부 라이브러리를 함께 이용할 때 사용할 수 있도록 Django는 개별적으로 CSRF 방지를 구현할 수 있는 방법도 제공하는데 지금은 CSRF 방지가 무엇인지 그리고 Django에서는 어떻게 기본적으로 구현할 수 있는지만 기억해주세요.

# 작성 페이지 만들기
1. Django는 CSRF를 방지할 수 있는 템플릿 태그를 제공합니다. {% csrf_token %}을 form에 작성하면 CSRF를 자동으로 방지하는 로직을 수행하게 됩니다.
```html
<!-- page_form.html -->
<form method="post">{% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="작성하기">
</form>
```

2. page_create뷰는 요청 방식(GET, POST)에 따라 수행하는 로직이 다릅니다.
### POST
먼저 POST 방식으로 요청이 들어왔을 때는 사용자가 폼에 데이터를 입력한 후 전송 버튼을 누른 것이므로 요청(request)으로 부터 데이터를 가져와서 데이터를 저장하고 저장된 데이터를 볼 수 있는 상세 일기 보기 페이지로 안내합니다.
```python
def page_create(request):
    if request.method == 'POST': # 만약 요청 방식이 POST라면
        new_page = Page( # 입력된 데이터를 가져와서 Page 데이터 모델을 만들고
            title=request.POST['title'],  
            content=request.POST['content'],
            feeling=request.POST['feeling'],
            score=request.POST['score'],
            dt_created=request.POST['dt_created']
        )
        new_page.save() # 데이터베이스에 저장한 후
        return redirect('page-detail', page_id=new_page.id) # 상세 일기 보기 페이지로 안내합니다.
```

이때 redirect에서 이동할 URL을 하드코딩 하는 것 대신 url-name을 사용하는 것이 권장되며 page-detail은 상세 보기를 할 데이터의 page_id가 필요하므로 키워드를 함께 전달합니다. 방금 우리가 생성한 Page 데이터 모델의 id값을 넘겨 주면 되겠죠?

### GET
GET 방식으로 요청이 들어왔을 때는 사용자가 처음 일기 작성 페이지에 들어왔을 때, 즉 입력할 폼을 요청할 때 입니다. 따라서 PageForm을 이용해서 새로운 form을 생성한 후 page_form 템플릿으로 생성한 form을 넘겨준 다음 템플릿과 함께 렌더해서 결과로 돌려 주도록 작성하면 됩니다.
```python
def page_create(request):
    if request.method == 'POST':
        ...
    else: # 만약 요청 방식이 GET이라면
        form = PageForm() # 새로운 form을 만들고 (빈 폼)
        return render(request, 'diary/page_form.html', {'form': form}) 
                # 템플릿으로 보내 렌더해서 결과로 돌려줍니다.
```

3. 개발 서버를 켜고 정상적으로 글이 작성되는지, 작성 후 상세 보기 페이지로 잘 이동하는지 확인해 주세요.

# Django Form Field
Django 폼(Form)을 작성할 때 가장 중요한 부분이 바로 데이터에 맞는 폼 필드를 작성하는 것입니다. Django는 입력 데이터에 따라 사용할 수 있는 여러 내장 폼 필드를 제공하는데, 각각의 폼 필드는 그에 맞는 입력 위젯을 기본으로 가지고 있습니다. 아래는 Django에서 제공하는 몇 가지 필드 목록과 옵션들 입니다.

|필드	|설명	|옵션	|기본 위젯|
|------|-------|-----|------|
|CharField	|문자열 입력을 위한 필드입니다.|	max_length : 최대 길이 설정 min_length : 최소 길이 설정 strip : 문자열 앞뒤 공백을 제거합니다. (기본값: True) empty_value : 비어 있는 값을 나타낼 값 (기본값: 빈 문자열)	|TextInput|
|EmailField	|이메일 입력을 위한 필드입니다.|	CharField와 같은 옵션인자를 사용합니다.|	EmailInput|
|IntegerField	|정수 입력을 위한 필드입니다.	|max_value : 최댓값 설정 min_value : 최솟값 설정	|NumberInput|
|BooleanField	|True, False 입력을 위한 필드입니다. (기본적으로 입력을 위해 체크박스가 사용됩니다.)|	체크박스가 빈 값일 경우 False로 처리됩니다.|	CheckboxInput|
|ChoiceField	|주어진 값 안에서 하나를 선택할 수 있는 형식의 필드입니다.	|choices : 선택 항목 들의 목록 인자로 각 선택 목록은 튜플 형식을 사용합니다. 예시: options = [('1', 'male'), ('2', 'female), ('3', 'other')]	|Select|
|MultipleChoiceField	|주어진 보기에서 여러개를 선택할 수 있는 형식의 필드입니다.|	ChoiceField와 같은 옵션인자를 사용합니다.|	SelectMultiple|
|DateField	|날짜 형식을 입력 받는 필드입니다.|	input_formats : 날짜의 형식을 지정합니다. (https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-DATE_INPUT_FORMATS)|	DateInput|
|TimeField	|시간 형식을 입력받는 필드입니다.|	DateField와 같은 옵션인자를 사용합니다.|	TimeInput|
|DateTimeField|	날짜/시간 형식을 입력 받는 필드입니다.|	DateField와 같은 옵션인자를 사용합니다.	|DateTimeInput|

- 이 밖에도 데이터 형식에 맞는 몇 가지 내장 필드가 있습니다. 내가 사용할 데이터에 대한 필드가 있는지 궁금할 때는 항상 공식문서를 참고하세요. https://docs.djangoproject.com/en/2.2/ref/forms/fields/#built-in-field-classes
- widget과 관련된 더 많은 내용은 아래 공식문서를 확인하세요. https://docs.djangoproject.com/en/2.2/ref/forms/widgets/
아래는 필드를 정의할 때 사용할 수 있는 필드 옵션들 입니다.

|인수	|설명|
|----|----|
|required|	필수적으로 입력해야 하는 항목 인지를 결정합니다. 기본값은 True이며 False일 경우 비워두는 것을 허용합니다.|
|label	|해당 필드의 label 항목에 적힐 이름을 지정합니다. 만약 지정하지 않을 경우 폼 필드를 지정한 변수명의 첫 글자를 대문자로, 밑줄(_)이 있다면 띄어쓰기로 변경하여 label 값으로 사용합니다.|
|label_suffix	|기본적으로 label 다음 콜론(:)이 붙어서 표시되는데 이 값을 변경합니다.|
|initial	|해당 필드에 초기값을 줄 때 사용합니다.|
|widget|	해당 필드가 사용할 사용자 입력 UI, 즉 위젯을 지정합니다. 기본적으로 각 데이터 항목에 맞는 기본 위젯이 설정되어 있습니다.|
|help_text	|입력에 도움이 되는 문자열을 입력 필드 밑에 표시합니다.|
|validators	|유효성 검증을 위한 검증 목록을 리스트 형태로 작성합니다.|
|disabled	|필드의 편집 가능 여부를 결정합니다. 기본 값은 False 이며 True일 경우 해당 필드가 보이지만 편집할 수 없습니다.|

- label
```python
# forms.py
from django import forms

class UserForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField(label='Your age')
```
```html
<!-- html -->
<label for="id_name">Name:</label> 
<input type="text" name="name" required id="id_name">
<label for="id_age">Your age:</label>
<input type="number" name="age" required id="id_age">
```

label_suffix
```python
# forms.py
from django import forms

class UserForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField(label_suffix='=')
```
```html
<!-- html -->
<label for="id_name">Name:</label>
<input type="text" name="name" required id="id_name">
<label for="id_age">Age=</label>
<input type="number" name="age" required id="id_age">
```

help_text
```python
# forms.py
from django import forms

class UserForm(forms.Form):
    name = forms.CharField(help_text='한글 이름을 작성해주세요.')
    age = forms.IntegerField()
```
```html
<!-- html -->
<label for="id_name">Name:</label>
<input type="text" name="name" required id="id_name">
<span class="helptext">한글 이름을 작성해주세요.</span>
<label for="id_age">Age:</label>
<input type="number" name="age" required id="id_age">
```

더 많은 필드 옵션이 궁금하다면 아래 공식 문서를 참고하세요.
https://docs.djangoproject.com/en/2.2/ref/forms/fields/#core-field-arguments

# Model Form 사용해서 구현
1. 지금 작성된 forms.py의 PageForm을 모델 폼(Model Form)으로 바꾸는 과정입니다. 먼저 forms.ModelForm을 상속받아 PageForm을 정의합니다.
```python
from django import forms

class PageForm(forms.ModelForm):
```

2. 모델 폼을 사용하는 것의 장점은 폼 필드를 각각 정의해 주지 않아도 모델의 필드를 보고 자동으로 Django가 유추해서 폼 필드를 만들어 준다는 것입니다. 이를 위해 Meta 클래스를 이용해 사용할 모델과 입력받을 모델 필드를 명시해 주어야 합니다.
```python
from django import forms
from .models import Page # 사용할 모델을 가져옵니다.

class PageForm(forms.ModelForm):

    class Meta:
        model = Page # 모델 폼에서 사용할 모델과 필드를 명시합니다.
        fields = ['title', 'content', 'feeling', 'score', 'dt_created']
```

3. PageForm을 모델 폼으로 변경 했으므로 page_create뷰의 로직도 수정해 주어야 합니다. POST 방식일 때의 로직에서 기존에는 request.POST로 부터 입력된 데이터를 하나씩 가져 왔지만 이제는 ModelForm을 사용 하기 때문에 Model과 Form이 서로 다루게 될 데이터의 형식을 알고 있는 상태이므로 아래와 같이 바로 바인딩 폼을 만들 수 있습니다. 그 후 바인딩 폼을 이용해 데이터를 저장하고 이때 반환 되는 데이터 모델을 new_page에 받아서 redirect의 page_id 값으로 사용합니다.
```python
def page_create(request):
    if request.method == 'POST':
        form = PageForm(request.POST) # 입력된 데이터와 폼을 합쳐서 바인딩 폼을 만듭니다.
        new_page = form.save() # 데이터 저장 및 생성된 데이터 모델 반환
        return redirect('page-detail', page_id=new_page.id)
        else:
            ...
```
```python
# 이전 코드
def page_create(request):
    if request.method == 'POST':
        new_page = Page( # 아래 부분이 ModelForm을 사용하면 간단해 집니다.
            title=request.POST['title'],
            content=request.POST['content'],
            feeling=request.POST['feeling'],
            score=request.POST['score'],
            dt_created=request.POST['dt_created']
        )
        new_page.save() # 여기서는 Page 모델을 이용한 저장로직
        return redirect('page-detail', page_id=new_page.id)
        else:
            ...
```

4. 개발 서버를 켜고 일기 작성 페이지로 간 다음 정상적으로 동작하는지 확인해 주세요.


# 유효성 검증
1. diary/validators.py에 유효성 검사를 위한 함수를 작성합니다.

   - 유효성 검사는 조건을 만족하지 못했을 경우 ValidationError를 발생시키면 됩니다.
   - 먼저 ValidationError를 import합니다.

```python
# validators.py

from django.core.exceptions import ValidationError
```

2. 입력된 값에 '#'이 포함되어 있는지를 검증하는 validate_no_hash() 함수를 작성합니다.

   - 함수를 정의하고 파라미터로 검증을 수행할 값을 받습니다.
   - 그 후 만약 해당 값에 '#'이 들어 있다면 raise문을 이용해서 ValidationError를 내도록 합니다.
   - 이때 에러 메시지를 함께 적어 줄 수 있습니다.

```python
from django.core.exceptions import ValidationError

def validate_no_hash(value):
    if '#' in value:
        raise ValidationError('# 은 포함될 수 없습니다.')
```

3. 다음으로 입력된 값에 숫자가 들어 있는지를 검증하는 validate_no_numbers() 함수를 작성합니다.
   - 입력된 값을 하나씩 반복하면서 isdigit()을 이용해 숫자인지 여부를 체크합니다.
   - 만약 해당 값이 숫자라면 ValidationError를 내도록 합니다.

```python
from django.core.exceptions import ValidationError

...

def validate_no_numbers(value):
    for ch in value:
        if ch.isdigit():
            raise ValidationError('숫자는 들어갈 수 없습니다.')
```

4. 마지막으로 입력된 값이 0부터 10사이의 숫자 인지를 검증하는 validate_score() 함수를 작성합니다.

```python
from django.core.exceptions import ValidationError

...

def validate_score(value):
    if value < 0 or value > 10:
        raise ValidationError('0부터 10사이의 숫자만 입력 가능합니다.')
```

5. 이제 작성한 validator들을 적용시켜 주면 됩니다.
    - 우리는 현재 모델 폼을 사용하고 있으므로 모델 필드에 유효성 검증을 추가해 주면 됩니다.
    - models.py로 가서 먼저 우리가 작성한 validator를 가져옵니다.

```python
from django.db import models
from .validators import validate_no_hash, validate_no_numbers, validate_score
```

- 각각의 필드에 맞는 유효성을 validators 파라미터로 전달합니다.
```python
from django.db import models
from .validators import validate_no_hash, validate_no_numbers, validate_score

# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=100, validators=[validate_no_hash])
    content = models.TextField(validators=[validate_no_hash])
    feeling = models.CharField(max_length=80, validators=[validate_no_hash, validate_no_numbers])
    score = models.IntegerField(validators=[validate_score])
    dt_created = models.DateField()

    def __str__(self):
        return self.title
```

6. 이제 views.py로 가서 입력된 데이터가 유효성 검증을 통과했을 때만 저장되도록 로직을 수정합니다.

```python
def page_create(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid(): # 데이터가 유효한 경우에만
            new_page = form.save() # 저장 로직을 수행하고
            return redirect('page-detail', page_id=new_page.id) # 새 페이지로 갑니다.
    else:
            ...
```

7. 그리고 만약 데이터가 유효하지 않다면 어떻게 해야 할까요? 다시 데이터를 입력하도록 하면 됩니다.
    - 데이터가 유효하지 않다면 page_form 템플릿에 바인딩 폼을 전달하여 데이터가 있는 상태로 다시 입력하도록 결과로 돌려줍니다.

```python
def page_create(request):
    if request.method == 'POST':
        form = PageForm(request.POST) # 이 form은 입력된 데이터가 들어있는 바인딩 폼입니다.
        if form.is_valid():
            new_page = form.save()
            return redirect('page-detail', page_id=new_page.id)
        else: # 데이터가 유효하지 않다면
            return render(request, 'diary/page_form.html', {'form': form})
    else:
        form = PageForm() # 이 form은 비어있는 폼 입니다.
        return render(request, 'diary/page_form.html', {'form': form})
```

- 위와 같은 코드는 아래처럼 다시 적을 수 있습니다.
- 데이터가 유효하지 않을 때의 else를 지우고 중복되는 return render (...)를 하나로 수행하도록 작성했습니다.
- 이렇게 하면 요청이 POST 방식이라면 입력된 데이터가 채워진 form을, GET 방식이라면 비어있는 form을 갖게 됩니다.

```python
def page_create(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            new_page = form.save()
            return redirect('page-detail', page_id=new_page.id)
    else:
        form = PageForm()
    return render(request, 'diary/page_form.html', {'form': form})
```

8. 개발 서버를 켜고 각각의 유효성 검증이 잘 동작 하는지 확인해 주세요.


# form에 css 입히기
1. 이번에는 일기 작성 페이지에 스타일을 입혀 보겠습니다.
- 먼저 page_form 템플릿으로 가서 템플릿 상속 및 {block} 처리해 주겠습니다.
```html
{% extends './base.html' %} <!-- [A] base 템플릿을 상속 합니다.-->

{% block content %} <!-- [B] content 블럭 처리 -->
<div class="wrap-post">
    <form method="post">{% csrf_token %}
        ...
    </form>
</div>
{% endblock content %} <!-- [B] content 블럭 처리 -->
```

- 다음으로 각각의 입력 필드를 작성하면 되는데 이러한 입력 필드는 page_create뷰에서 넘겨준 form으로 접근할 수 있습니다.
- 지금 작성하는 class나 div 등의 구조는 미리 작성해 놓은 styles.css를 따른 것입니다. 이러한 부분들은 다양한 디자인 템플릿에 맞게 매번 변경되기 때문에 우리가 템플릿 언어로 작성해서 여러 데이터나 컴포넌트를 템플릿에 적용하는 과정을 이해하는 것이 중요합니다.
```html
{% extends './base.html' %}

{% block content %} 
<div class="wrap-post">
    <form method="post">{% csrf_token %}
        <div class="editor">

            <div class="input input-date">
                <p>날짜</p>
                {{form.dt_created}} <!-- [C] 날짜 입력 필드-->
            </div>

            <div class="input input-score">
                <p>감정 점수</p>
                {{form.score}} <!-- [D] 감정 점수 입력 필드-->
            </div>

            <div class="input input-title">
                <p>제목</p>
                {{form.title}} <!-- [E] 제목 입력 필드-->
            </div>

            <div class="input input-state">
                <p>상태</p>
                {{form.feeling}} <!-- [F] 감정 상태 입력 필드-->
            </div>

            {{form.content}} <!-- [G] 일기 내용 입력 필드-->

            <div class="post-btn">
                <input type="submit" value="작성완료">
            </div>
            
        </div>
    </form>
</div>
{% endblock content %} 
```

2. 개발 서버를 켜고 일기 작성 페이지로 들어가보면 디자인이 적용되어 있는 것을 확인할 수 있습니다.

3. 이전에는 {{ form.as_p }}를 통해 Django가 제공하는 템플릿 형식을 따랐기 때문에 에러 메시지가 표시 되었지만 이제는 우리가 각각의 폼 요소들을 따로 가져다 쓰고 있으므로 에러 메시지가 표시 될 수 있도록 작성해 주어야 합니다.
- 에러 메시지는 아래와 같이 각각의 필드 안의 errors를 이용해서 반복 표시되도록 구현합니다.
- 하나의 필드에 대해 여러가지 에러가 나올 수 있기 때문입니다.

```html
{% for error in example_field.errors %}
    <span>{{error}}</span>
{% endfor %}
```

- 각각의 필드에 대해 작성해 줍니다.
```html
{% extends './base.html' %}

{% block content %}
<div class="wrap-post">
    <form method="post">{% csrf_token %}
        <div class="editor">
            <div class="input input-date"><p>날짜</p>{{form.dt_created}}</div>

            <div class="input input-score">
                <p>감정 점수</p>
                {{form.score}}
                {% for error in form.score.errors %} <!-- 에러메시지 작성 -->
                    <span>{{error}}</span>
                {% endfor %}
            </div>
             
            <div class="input input-title">
                <p>제목</p>
                {{form.title}}
                {% for error in form.title.errors %} <!-- 에러메시지 작성 -->
                    <span>{{error}}</span>
                {% endfor %}
            </div>
            
            <div class="input input-state">
                <p>상태</p>
                {{form.feeling}}
                {% for error in form.feeling.errors %} <!-- 에러메시지 작성 -->
                    <span>{{error}}</span> 
                {% endfor %}
            </div>
            
            {{form.content}}
            {% for error in form.content.errors %} <!-- 에러메시지 작성 -->
                <span>{{error}}</span>
            {% endfor %}

            <div class="post-btn">
                <input type="submit" value="작성완료">
            </div>
        </div>
    </form>
</div>
{% endblock content %}
```

개발 서버를 켜고 유효성 검증에 실패했을 때 아래와 같이 에러 메시지가 잘 나오는지 확인합니다.

# 수정 기능
1. 이번에는 수정하기 기능을 구현해 보도록 하겠습니다. 먼저 urls.py로 가서 page-update를 주석 해제해 주세요.
```python
from django.urls import path
from . import views

urlpatterns = [
    path('diary/', views.page_list, name='page-list'),
    path('diary/info', views.info, name='info'),
    path('diary/write/', views.page_create, name='page-create'),
    path('diary/page/<int:page_id>/', views.page_detail, name='page-detail'),
    path('diary/page/<int:page_id>/edit/', views.page_update, name='page-update'),
    # path('diary/page/<int:page_id>/delete/', views.page_delete, name='page-delete'),
]
```

2. page_detail 템플릿으로 가서 수정하기로 가는 링크를 작성해 주겠습니다. {url} 템플릿 태그를 이용해서 작성하면 되겠죠? 이때 수정할 데이터를 조회해야 하므로 조회를 위한 object.id도 함께 적어 줍니다.
```python
{% extends './base.html' %}

{% block content %}
<div class="wrap-notetext">
    <div class="notetext">
        <div class="text-box">
           ...
            <div class="notetext-btn">
                <ul>
                    <li><a href="#">삭제하기</a></li>
                    <li><a href="{% url 'page-update' object.id %}">수정하기</a></li>
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

3. views.py로 가서 page_update뷰를 작성해 보겠습니다.
   - page_update뷰는 request와 page_id 파라미터가 필요합니다.
   - 이 page_id를 사용해서 수정할 Page 데이터 모델을 조회합니다.

```python
def page_update(request, page_id):
    object = Page.objects.get(id=page_id)
```

### POST
- 요청이 POST 방식 이라는 것은 사용자가 데이터를 수정하고 제출을 했다는 것을 의미합니다. 우리는 입력된 데이터를 받아서 유효성을 검사하고 데이터베이스에 저장한 후 일기 상세 보기 페이지로 안내하면 됩니다.
- Create와 달리 Update는 새로 Page 데이터 모델을 만들어서 저장하는 것이 아니라 기존의 데이터 모델을 수정해야 하므로 PageForm의 instance 파라미터로 조회한 데이터 모델을 넘겨 주어야 합니다.

```python
def page_update(request, page_id):
    object = Page.objects.get(id=page_id)
    if request.method == 'POST': # 요청이 POST 방식이라면
        form = PageForm(request.POST, instance=object) # 기존의 데이터 모델에 새로운 데이터를 설정하고
        if form.is_valid(): # 유효성 검사를 통과했다면
            form.save() # 데이터를 저장한 뒤
            return redirect('page-detail', page_id=object.id) # 상세 보기 페이지로 안내합니다.
```
  
### GET
- 요청이 GET 방식 이라는 것은 사용자가 처음 수정하기 페이지에 왔을 때를 의미합니다.
- 이때 우리는 비어있는 폼 형식의 페이지가 아니라 기존 데이터가 채워진 상태의 폼을 제공해야 하므로 PageForm의 instance 파라미터에 조회한 Page 데이터 모델을 넘겨줍니다.

```python
def page_update(request, page_id):
    object = Page.objects.get(id=page_id)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect('page-detail', page_id=object.id)
    else:
        form = PageForm(instance=object)
```

### return
- 마지막으로 POST와 GET에서 작성한 form을 이용해서 page_form 템플릿을 렌더한 후 결과로 돌려주도록 작성합니다.
- 이렇게 하게 되면 요청 방식이 POST 일 때는 form이 입력된 데이터가 들어간 form이 되고 만약 데이터가 유효하다면 데이터를 저장하고 상세 페이지로 가며, 유효하지 않다면 form에 입력된 데이터를 갖고 있는 그대로 return을 향하게 됩니다.
- 요청 방식이 GET 방식 일 때는 폼에 기존 데이터를 넣은 후 다른 로직이 없으므로 return을 향하게 되는거죠.
- 그러면 return에서는 각각 작성된 form을 page_form 템플릿으로 넘겨서 렌더한 후 결과로 돌려주면 됩니다.

```python
def page_update(request, page_id):
    object = Page.objects.get(id=page_id)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect('page-detail', page_id=object.id)
    else:
        form = PageForm(instance=object)
    return render(request, 'diary/page_form.html', {'form': form})
```

4. 개발 서버를 켜고 상세 일기 보기 페이지로 가서 정상적으로 수정이 되는지 확인해 주세요.


# 삭제 기능
1. 이번에는 삭제 기능을 구현해 보겠습니다. 먼저 urls.py로 가서 page-delete에 해당 하는 URL의 주석을 해제합니다.

urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('diary/', views.page_list, name='page-list'),
    path('diary/info', views.info, name='info'),
    path('diary/write/', views.page_create, name='page-create'),
    path('diary/page/<int:page_id>/', views.page_detail, name='page-detail'),
    path('diary/page/<int:page_id>/edit/', views.page_update, name='page-update'),
    path('diary/page/<int:page_id>/delete/', views.page_delete, name='page-delete'),
]
```

2. 다음으로 page_detail 템플릿으로 가서 '삭제하기'를 누르면 삭제 페이지로 올 수 있도록 링크를 작성합니다. {url} 템플릿 태그를 이용하면 되는데 이때 삭제할 데이터를 조회할 page_id를 파라미터로 넘겨줍니다.

page_detail.html

```html
{% extends './base.html' %}

{% block content %}
<div class="wrap-notetext">
    <div class="notetext">
        ...
            <div class="notetext-btn">
                <ul>
                    <li><a href="{% url 'page-delete' object.id %}">삭제하기</a></li>
                    <li><a href="{% url 'page-update' object.id %}">수정하기</a></li>
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

3. 이제 page_delete뷰를 작성하겠습니다.
- page_delete뷰를 정의하는데 request와 page_id를 파라미터로 합니다.
- 그리고 이 page_id를 이용해서 삭제 처리할 Page 데이터를 조회합니다.

```python
def page_delete(request, page_id):
    object = Page.objects.get(id=page_id)
```

### POST
- 요청 방식이 POST 라는 것은 사용자가 삭제할 것 인지를 묻는 항목에 '예'를 눌러서 폼을 제출 했을 때를 말합니다.
- 조회한 데이터를 지우고 일기 목록 보기 페이지로 안내합니다.

```python
def page_delete(request, page_id):
    object = Page.objects.get(id=page_id)
    if request.method == 'POST': # 만약 요청 방식이 POST라면
        object.delete() # 조회한 Page 데이터를 삭제처리하고
        return redirect('page-list') # 일기 목록 보기로 안내합니다.
```

   
### GET
- 요청 방식이 GET이라는 것은 사용자가 처음 삭제하기를 눌렀을 때를 말합니다. 우리는 다시 한번 정말 삭제할 것인지를 물어보는 page_confirm_delete 템플릿을 렌더해서 결과로 돌려주면 됩니다.

```python
def page_delete(request, page_id):
    object = Page.objects.get(id=page_id)
    if request.method == 'POST':
        object.delete()
        return redirect('page-list')
    else: # 만약 요청이 GET 방식이라면
                # page_confirm_delete.html을 렌더해서 돌려주도록 합니다.
                # 이때 삭제 확인 페이지에서 글의 제목을 보여줄 수 있도록 object를 함께 넘겨줍니다.
        return render(request, 'diary/page_confirm_delete.html', {'object': object})
```

4. page_confirm_delete 템플릿으로 가서 먼저 상속과 {block} 처리해 주도록 하겠습니다.

```html
{% extends './base.html' %} <!-- [A] base 템플릿 상속 -->

{% block content %} <!-- [B] content 블럭 처리 -->
<div class="wrap-delete">
    <div class="delete-box">
        ...
    </div>
</div>
{% endblock content %} <!-- [B] content 블럭 처리 -->
```

- 그 다음 page_delete뷰에서 넘겨준 데이터를 이용해 작성된 날짜와 제목을 표시하고
- '남기기'를 누르면 다시 이 글의 상세 보기 페이지로 이동하도록 {url} 템플릿 태그를 이용해서 작성합니다.

```html
{% extends './base.html' %}

{% block content %}
<div class="wrap-delete">
    <div class="delete-box">
        <div class="note-info">
            <p>&#123;</p>
            <span class="note-date">{{object.dt_create}}</span>
            <span class="note-title">{{object.title}}</span>
            <p>&#125;</p>
        </div>
        <p>이 하루를 지울까요?</p>
        <form method='post'>{% csrf_token %}
            <ul>
                <li><input type="submit" value="지우기"></li>
                <li><a href="{% url 'page-detail' object.id%}">남기기</a></li> 
            </ul>
        </form>
    </div>
</div>
{% endblock content %}
```

개발 서버를 켜고 정상적으로 삭제 처리가 되는지 확인해 주세요.


# 메인 Url 설정
1. 감정 일기의 홈 화면을 만들어 보겠습니다. 먼저 urls.py로 가서 ''(빈 문자열)과 매칭이 되면 index뷰를 연결하도록 작성합니다.
- 이렇게 작성하면 이제 아무런 경로(path)가 안붙은 localhost:8000/ 와 같은 주소가 바로 index뷰로 연결됩니다.

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # 작성
    path('diary/', views.page_list, name='page-list'),
    path('diary/info', views.info, name='info'),
    path('diary/write/', views.page_create, name='page-create'),
    path('diary/page/<int:page_id>/', views.page_detail, name='page-detail'),
    path('diary/page/<int:page_id>/edit/', views.page_update, name='page-update'),
    path('diary/page/<int:page_id>/delete/', views.page_delete, name='page-delete'),
]
```

2. views.py로 가서 이제 index뷰를 작성합니다. index뷰는 index 템플릿을 렌더해서 결과로 돌려주는 간단한 뷰입니다.

```python
def index(request):
    return render(request, 'diary/index.html')
```

3. 마지막으로 index 템플릿으로 가서
- 정적 파일을 사용하기 위한 {load static} 템플릿 태그를 작성하고, styles.css를 {static} 템플릿 태그를 이용해서 작성합니다.
- 'Click to Enter'를 클릭하면 일기 목록 보기 페이지로 가도록 링크를 작성합니다.

```html
{% load static %} <!-- [A] -->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Mind Note</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="{% static 'diary/css/styles.css' %}"> <!-- [B] -->
    <link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/moonspam/NanumSquare/master/nanumsquare.css">
</head>
<body>
    <div class="wrap-intro">
        <h1><img src="{% static 'diary/image/logo01.svg' %}"></h1>
        <p>사람들은 익숙한 것에 끌립니다.<br>긍정적인 감정 습관을 기르고 행복에 익숙해지세요.</p>
        <a href="{% url 'page-list' %}">click to enter</a> <!-- [C] -->
    </div>
</body>
</html>
```

4. 개발 서버를 켜고 도메인으로 바로 접속해서 메인 페이지가 잘 나오는지 확인하고 'click to enter'를 눌러 일기 목록 보기 페이지로 가는지 확인합니다.


# 데이터가 없는 경우

1. page_list 템플릿을 보면 아래에 object_list에 데이터가 없을 때 보여줄 HTML이 있습니다.

```html
<div class="wrap-default">
    <div class="default">
        <div class="default-box">
            <p>"오늘 하루는 어땠나요? 당신의 하루를 들려주세요"</p>
            <a href="일기 작성 페이지로 이동하는 링크">일기쓰기</a>
        </div>
    </div>
</div>
```

2. object_list가 있으면 현재의 content 블럭 안의 내용을 보여 주도록 작성합니다.

```html
{% extends './base.html' %}

{% block content %}
{% if object_list %} <!-- 데이터가 있다면, 아래의 HTML이 나옵니다.-->
    <div class="wrap-note">
        <div class="note">         
            <div class="note-list">
                <ul>
                    {% for obj in object_list %}
                    <li>
                        <a href="{% url 'page-detail' obj.id %}">
                            <div class="date">
                                <span>{{obj.dt_created|date:"d"}}</span>
                                <p>{{obj.dt_created|date:"M"}}</p>
                            </div>
                            <h2>{{obj.title}}</h2>
                            <div class="score">
                                <p>감정점수</p>
                                <span>{{obj.score}}점</span>
                            </div>
                        </a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>
{% endif %} <!-- if 템플릿태그는 닫는 endif와 짝을 이룹니다. -->
{% endblock content %}
```

- 다음으로 object_list에 데이터가 없다면 페이지 아래의 HTML 코드가 나오도록 작성합니다.
- 일기 작성 페이지로 이동하는 링크도 작성합니다.
```html
{% extends './base.html' %}

{% block content %}
{% if object_list %}
    <div class="wrap-note">
        <div class="note">         
            <div class="note-list">
                ...
            </div>
        </div>
    </div>
{% else %} <!-- else 즉, object_list에 데이터가 없을 때 -->
    <div class="wrap-default">
        <div class="default">
            <div class="default-box">
                <p>"오늘 하루는 어땠나요? 당신의 하루를 들려주세요"</p>
                <a href="{% url 'page-create' %}">일기쓰기</a> <!-- 일기 작성 페이지로 가는 링크 -->
            </div>
        </div>
    </div>
{% endif %}
{% endblock content %}
```

4. 개발 서버를 켜고 모든 데이터가 없을 때 아래와 같이 잘 표시 되는지 확인합니다.


# seed 데이터 추가 및 추가 이후 유효성 검사

1. django-seed를 사용하기 위해서는 settings.py의 INSTALLED_APPS 항목에 django_seed를 추가해 주어야합니다.
```python
# settings.py
...
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'diary',
    'django_seed', # 추가합니다.
]
...
```

2. 터미널을 열고 django-seed를 이용해서 무작위의 30개 Page 데이터를 생성합니다. manage.py 다음 seed를 적고 데이터를 생성할 앱 이름과 생성할 숫자를 적어 주면 됩니다.

```python
python manage.py seed diary --number=30
```

3. 개발 서버를 켜고 일기 목록 보기 페이지로 가면 생성된 데이터를 확인할 수 있습니다. 그런데 보면 감정 점수가 정수형 이긴 하지만 범위가 너무 넓습니다. 이를 해결 하기 위한 validate_pages() 함수를 구현해 볼게요.

4. diary 앱의 validate_data.py에 validate_pages() 함수를 정의합니다.
- 데이터를 조회하기 위해 먼저 Page 모델을 import합니다.
- 모든 데이터를 가져와서 pages라는 변수에 넣습니다.

```python
from .models import Page

def validate_pages():
    pages = Page.objects.all()
```

- pages를 하나씩 반복하면서 안쪽의 score가 0미만 이거나 10을 초과하는지 확인합니다.
- 만약 0미만 이거나 10을 초과한다면 random 모듈을 이용해 0에서 10사이의 무작위 정수를 생성한 뒤 수정하고 저장합니다.

```python
from .models import Page
import random # random 모듈 import

def validate_pages():
    pages = Page.objects.all()
    for page in pages:
        if page.score < 0 or page.score > 10: # 만약 범위를 벗어난다면
            page.score = random.randint(0, 10) # 0~10 사이의 무작위 정수로 수정하고
            page.save() # 저장합니다.
```

5. 이제 작성한 validate_pages() 함수를 한 번만 실행하면 모든 데이터의 score가 알맞게 변경됩니다.
- django shell을 실행하고 validate_pages() 함수를 import합니다.
- 가져온 함수를 실행해서 데이터를 변경합니다.
```shell
python manage.py shell
```

```python
from diary.validate_data import validate_pages

validate_pages()
```

6. 개발 서버를 켜고 일기 목록 페이지로 가서 정상적으로 감정 점수 값이 수정되었는지 확인합니다.


# 페이지네이션(Pagination) 정리하기
페이지네이션이란 데이터를 일정 길이로 나누어서 전달하는 기능입니다. 일반적으로 가지고 있는 데이터가 한 화면에 모두 보여 주기에 너무 많은 경우 사용하죠. 우리가 여러 웹 페이지에서 '이전 페이지로 가기' 또는  '다음 페이지로 가기' 등으로 자주 볼 수 있는 기능입니다.

페이지네이션은 프론트엔드와 백엔드에서 모두 구현이 필요합니다. 백엔드에서는 페이지 별 데이터를 데이터베이스로부터 가져와서 프론트에게 넘겨 주어야 하고 프론트엔드에서는 받은 데이터 목록과 페이지에 대한 정보를 화면에 표시하도록 만들어 주어야 합니다.

### Django의 페이지네이션

Django는 페이지네이션을 쉽게 구현할 수 있도록 하는 Paginator를 제공합니다. Paginator는 총 두 개의 파라미터만 넘겨주면 쉽게 정의할 수 있는데 첫 번째 파라미터는 각각의 페이지로 나뉘게 될 데이터의 목록, 두 번째 파라미터는 한 페이지에 보여줄 데이터의 수입니다.

```python
from django.core.paginator import Paginator # Django의 Paginator
from .models import Post # 작성한 모델 클래스

posts = Post.object.all() # 모든 데이터를 가져와서
paginator = Paginator(posts, 6) 
# 첫 번째 파라미터 : 페이지로 나뉘게 될 데이터의 목록
# 두 번째 파라미터 :  한 페이지에 보옂루 데이터의 수
```

이렇게 만들어진 Paginator는 자동으로 데이터를 개수에 따라 페이지를 나누어서 갖고 있고 우리는 페이지의 번호를 이용해서 Paginator로부터 페이지를 가져와서 제공하는 여러 기능을 사용하면 됩니다. Paginator와 각각의 Page가 가지고 있는 기능 중 자주 사용하는 것은 아래와 같습니다.

|메소드&속성	|설명	|예시|
|----|----|----|
|{paginator}.count	|paginator가 가지고 있는 데이터의 개수	|{paginator}.count|
|{paginator}.num_pages	|paginator가 가지고 있는 모든 페이지 수	|{paginator}.num_pages|
|{paginator}.page_range	|paginator가 가지고 있는 페이지의 범위(range)|	{paginator}.page_range|
|{paginator}.page(num)	|paginator가 가지고 있는 페이지 중 num번째 페이지 객체|	{paginator}.page(1)|
|{page}.has_next()	|page객체가 다음 페이지가 있는지 여부|	{page}.has_next()|
|{page}.has_previous()	|page객체가 이전 페이지가 있는지 여부	|{page}.has_previous()|
|{page.has_other_pages()|	page객체가 다른 페이지를 가지고 있는지 여부|	{page}.has_other_pages()|
|{page}.number	|page객체의 현재 페이지 번호	|{page}.number|
|{page}.object_list|	page객체가 가지고 있는 데이터 목록	|{page}.object_list|
|{page}.paginator|	page객체의 Paginator	|{page}.paginator|
|{page}.next_page_number()|	page객체의 다음 페이지 번호|	{page}.next_page_number()|
|{page}.previous_page_number()	|page객체의 이전 페이지 번호	|{page}.previous_page_number()|
|{page}.start_index()|	page객체가 가지고 있는 데이터의 시작 index (시작 index가 0이 아닌 1 기준)	|{page}.start_index()|
|{page}.end_index()|	page객체가 가지고 있는 데이터의 끝 index (시작 index가 0이 아닌 1 기준)|	{page}.end_index()|

이와 같은 메소드들을 이용하면 쉽게 페이지네이션을 구현할 수 있습니다. 그럼 View와 Template로 나누어 페이지네이션을 구현해 보겠습니다.

#### View 작성하기
Django 페이지네이션은 Paginator를 이용해서 구현합니다.
```python
from django.core.paginator import Paginator
```

먼저 페이지네이션을 구현하려면 데이터를 가져와야겠죠? 모델(Model)을 이용해서 가져오면 됩니다.

```python
def post_list(request):
    posts = Post.object.all() # 모든 Post 데이터를 가져옵니다.
```

그 다음은 Django의 Paginator에 페이지네이션을 구현할 데이터 목록과 각 페이지마다 보여줄 데이터의 개수를 전달합니다.

```python
def post_list(request):
    posts = Post.object.all() 
    paginator = Paginator(posts, 8) # Post를 한 페이지에 8개씩 할당합니다.
```

그리고 이제 이 paginator 안에 있는 여러 유용한 메소드를 이용해서 구현하면 됩니다.

이제 Template으로 넘겨주기 위한 페이지를 Paginator로 부터 가져와야 합니다. 이때 가져올 페이지의 번호는 URL의 쿼리스트링에 있는 데이터를 이용하겠습니다.

```python
def post_list(request):
    posts = Post.object.all() 
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page') # 쿼리 스트링으로 부터 페이지 번호 조회
```

그 후 .page(num) 메소드를 이용해서 페이지를 가져온 후 Template으로 넘겨줍니다.

```python
def post_list(request):
    posts = Post.object.all() 
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.page(page_number) # 페이지 번호에 해당하는 페이지를 가져옴
    return render(request, 'post_list.html', {'page_obj': page_obj})
```

#### Template 작성하기
Template에서는 View에서 넘어온 Page를 이용해서 화면을 구성하면 됩니다. 먼저 페이지의 모든 데이터를 표시할 때는 아래와 같이 for 템플릿 태그를 이용해서 작성할 수 있습니다.

```html
...

{% for post in page_obj.object_list %}
    <p>post로 부터 조회한 데이터</p>
    <p>{{ post.title }}</p>
{% endfor %}

...
```

그리고 이전 페이지, 다음 페이지로 가는 오브젝트들도 Page가 제공하는 메소드를 이용하면 쉽게 구현할 수 있습니다.
```html
...

{% if page_obj.has_previous %} <!-- 만약 현재 페이지의 이전 페이지가 있다면 -->
    <a href="?page=1"> first</a>
    <a href="?page={{ page_obj.previous_page_number }}">prev</a> <!-- 이전 페이지 번호 -->
{% endif %}

<span>
    Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
    <!-- page_obj.number : 페이지(page_obj)의 번호 -->
    <!-- page_obj.paginator.num_pages : 페이지를 관리하는 Paginator가 가지고 있는 전체 페이지 수 -->
</span>

{% if page_obj.has_next %} <!-- 만약 현재 페이지의 다음 페이지가 있다면 -->
    <a href="?page={{ page_obj.next_page_number }}">next</a> <!-- 다음 페이지 번호 -->
    <a href="?page={{ page_obj.paginator.num_pages }}">last </a> <!-- 전체 페이지의 개수 = 마지막 페이지 번호 -->
{% endif %}

...
```
이외에 Django의 Pagination에 대해 더 많이 알고 싶다면 아래 공식문서를 참고하세요.
https://docs.djangoproject.com/en/2.2/topics/pagination/

# pagination 구현
지금은 하나의 페이지에 너무 많은 일기가 나오고 있어요. 아래를 참고해서 한 페이지에 8개씩 일기가 나누어 나오도록 페이지네이션(Pagination)을 구현해 주세요.

### view 구현하기
먼저 django로 부터 paginator를 가져옵니다.
```python
from django.core.paginator import Paginator
```

page_list뷰에 조회한 모든 데이터를 이용해서 Paginator를 생성합니다.

```python
paginator = Paginator(<페이지네이션을 구현할 데이터>, <한 페이지에 보여줄 개수>)
```

현재 들어온 요청(request)의 쿼리스트링으로부터 보여 줄 페이지의 번호를 가져와 주세요. 쿼리스트링의 페이지 번호에 대한 키워드 값은 page 입니다.

```python
request.GET.get('<keyword>')
```

가져온 페이지 번호가 None이라면 조회할 페이지 가 첫 페이지가 되도록 페이지 번호가 1이 되도록 작성해 주세요.
```python
def page_list(request):
    object_list = Page.objects.all()
    paginator = # Paginator 생성
    curr_page_num = # 쿼리스트링에서 가져온 현재 페이지 번호
        if <가져온 페이지 번호가 None이라면>:
            <첫 페이지가 되도록 합니다.>
    return render(request, 'diary/page_list.html', {'object_list': object_list})
```

페이지네이터로 부터 보여줄 페이지를 가져와 주세요.

```python
<paginator>.page(<조회할 페이지 번호>)
```

기존의 모든 데이터(object_list) 대신 Paginator에서 가져온 현재 페이지를 템플릿으로 넘겨주세요. 이때 키워드는 page를 사용해 주세요.

### Template 구현하기
page_list.html로 가서 [A]~[J]를 구현해 주세요.

[A] object_list 대신 뷰에서 넘어온 page안에 데이터가 있는지 여부로 수정해 주세요.
```python
<현재 페이지>.object_list
```

[B]  object_list 대신 page안의 데이터를 사용하도록 수정해 주세요.

[C] 페이지네이터를 구현합니다. 페이지 하단의 comments를 복사해서 붙여 넣어 사용해 주세요.

### 이전 페이지 구현하기
[D] 현재 페이지 이전의 페이지가 있을 때, 처음으로 가는 링크와 이전 페이지로 가는 링크를 작성해 주세요.
```html
{% if <현재 페이지>.has_previous %}
{% endif %}
```

[E], [F] 쿼리스트링으로 알맞은 페이지 번호를 전달하도록 작성해 주세요.

쿼리 스트링은 ?로 시작하며 key와 value로 이루어져 있습니다.
```html
?<key>=<value>
```
현재 페이지의 이전 페이지 번호는 'previous_page_number'를 이용하면 됩니다.
```html
{{ <현재 페이지>.previous_page_number }}
```

### 현재 페이지 구현하기
[G]  현재 페이지 번호와 전체 페이지 번호를 이용해서 작성해 주세요.
```html
<p> <현재 페이지 번호> of <전체 페이지 번호> </p>
```

현재 페이지 번호는 현재 페이지에 'number' 를 이용해서 가져올 수 있습니다.
```python
<현재 페이지>.number
```
전체 페이지 번호는 현재 페이지가 아닌 페이지네이터(paginator)객체를 통해서 가져올 수 있습니다.
```python
<현재 페이지>.paginator.num_pages
```

### 다음 페이지 구현하기
[H]  현재 페이지 다음의 페이지가 있을 때, 다음 페이지로 가는 링크와 마지막 페이지로 가는 링크를 작성해 주세요.
```html
{% if <현재 페이지>.has_next %}
{% endif %}
```

[I], [J] 쿼리스트링으로 알맞은 페이지 번호를 전달하도록 작성해 주세요.

현재 페이지의 다음 페이지 번호는 'next_page_number'를 이용하면 됩니다.
```html
{{ <현재 페이지>.next_page_number }}
```

개발 서버를 켜고 페이지네이션이 잘 구현 되었는지 확인해 주세요.


## 해설

### View 구현하기
1. 먼저 Paginator를 import합니다.
```python
from django.core.paginator import Paginator
```

page_list 뷰에 Paginator를 생성합니다.  
Paginator는 첫 번째 파라미터로 페이지를 나눌 데이터 목록을, 두 번째 파라미터로는 한 페이지에 표시할 데이터의 개수를 받습니다.
```python
def page_list(request):
    object_list = Page.objects.all()
    paginator = Paginator(object_list, 8) # Paginator 생성
    return render(request, 'diary/page_list.html', {'object_list': object_list})
```

현재 보여줄 페이지의 번호를 쿼리스트링으로부터 가져옵니다.
```python
def page_list(request):
    object_list = Page.objects.all()
    paginator = Paginator(object_list, 8)
        curr_page_number = request.GET.get('page') # 쿼리스트링 데이터 중 'page'의 값을 가져옵니다.
    return render(request, 'diary/page_list.html', {'object_list': object_list})
```

만약 curr_page_number가 None일 경우, 즉 처음으로 일기 목록 페이지에 접근해서 쿼리스트링의 데이터 중 page의 값이 없을 때는 첫 페이지로 설정 되도록 curr_page_number를 1로 설정합니다.
```python
def page_list(request):
    object_list = Page.objects.all()
    paginator = Paginator(object_list, 8)
    curr_page_num = request.GET.get('page')
    if curr_page_num is None: # 만약 쿼리스트링에 'page'가 없어서 None이 설정되었다면 
        curr_page_num = 1 # 첫 번째 페이지를 가리키는 1로 바꿔줍니다.
    return render(request, 'diary/page_list.html', {'object_list': object_list})
```

이제 curr_page_num을 이용해서 Paginator로 부터 해당 번호의 페이지를 가져오면 됩니다.
```python
def page_list(request):
    object_list = Page.objects.all()
    paginator = Paginator(object_list, 8)
    curr_page_num = request.GET.get('page')
    if curr_page_num is None:
        curr_page_num = 1
    page = paginator.page(curr_page_num) # Paginator로 부터 하나의 페이지를 가져옵니다.
    return render(request, 'diary/page_list.html', {'object_list': object_list})
```

그리고 가져온 페이지를 page_list 템플릿으로 넘겨줍니다. 지금은 모든 page 데이터를 넘겨주고 있지만 이제는 모든 데이터를 한 번에 표시하는 것이 아니라 하나의 페이지에 있는 데이터만 보여줄 것이기 때문입니다.
```python
def page_list(request):
    object_list = Page.objects.all()
    paginator = Paginator(object_list, 8)
    curr_page_num = request.GET.get('page')
    if curr_page_num is None:
        curr_page_num = 1
    page = paginator.page(curr_page_num)
    return render(request, 'diary/page_list.html', {'page': page}) # 이제는 페이지를 넘겨줍니다.
```

### Template 구현하기
이제 page_list 템플릿에 pagination을 적용해 주겠습니다.  
먼저 기존의 모든 데이터를 가져와서 사용하는 부분 대신 page 안에 있는 데이터를 사용하도록 수정해 주겠습니다.
```html
{% extends './base.html' %}

{% block content %}
{% if page.object_list %} <!-- [A] object_list 대신 page.object_list 로 수정 -->
    <div class="wrap-note">
        <div class="note">         
            <div class="note-list">
                <ul>
                    {% for obj in page.object_list %} <!-- [B] object_list 대신 page.object_list 로 수정 -->
                    <li>
                       ...
                    </li>
                    {% endfor %}
                </ul>
            </div>
           ...
{% endif %}
{% endblock content %}
```

그 다음 페이지 아래 있는 pagination을 위한 코드를 복사해서 [C]위치에 넣어주겠습니다.
```html
{% extends './base.html' %}

{% block content %}
{% if page.object_list %}
    <div class="wrap-note">
        <div class="note">         
            <div class="note-list">
                <ul>
                    {% for obj in page.object_list %}
                    ...
                    {% endfor %}
                </ul>
            </div>
            <!-- [C] 이곳에 페이지네이션을 붙여 넣어줍니다. -->
                        <div class="paging">
                        {% if [D] %}
                            <a href="[E]" class="first">처음</a>
                            <a href="[F]" class="prev">이전</a>
                        {% endif %}
                    
                        <span class="page">
                            <p>[G]</p>
                        </span>
                    
                        {% if [H] %}
                            <a href="[I]" class="next">다음</a>
                            <a href="[J]" class="last">마지막</a>
                        {% endif %}
                    </div>
        </div>
    </div>
{% else %}
    ...
{% endif %}
{% endblock content %}
```

### 이전 페이지 구현하기
[D] 현재 페이지의 이전에 페이지가 있는지를 <page>.has_previous를 이용해 체크하고 만약 있다면 쿼리스트링을 이용해서 처음으로 가는 링크와 이전 페이지로 가는 링크를 작성해 줍니다.  
처음으로 가는 페이지 번호는 1이지만 이전 페이지의 페이지 번호는 현재 페이지를 기준으로 해야 하므로 <page>.previous_page_number 객체를 이용합니다.

```html
...
<div class="paging">
  {% if page.has_previous %}
      <a href="?page=1" class="first">처음</a>
      <a href="?page={{page.previous_page_number}}" class="prev">이전</a>
  {% endif %}

  <span class="page">
      <p>[G]</p>
  </span>

  {% if [H] %}
      <a href="[I]" class="next">다음</a>
      <a href="[J]" class="last">마지막</a>
  {% endif %}
</div>
...
```

### 현재 페이지 구현하기
전체 페이지 중 현재 몇 번째 페이지에 있는지를 보여주는 부분을 작성해 주겠습니다.

[G] 위치에 <현재 페이지 번호> of <전체 페이지 번호> 형식으로 만들어 주면 되는데 현재 페이지 번호는 <page>.number를 사용하면 되지만 전체 페이지 번호는 전체 페이지 개수와 같은 값으로 현재의 페이지가 아닌 paginator가 가지고 있는 값입니다.

<page>.paginator.num_pages를 이용해서 전체 페이지 번호를 알 수 있습니다.
```html
...
<div class="paging">
  {% if page.has_previous %}
      <a href="?page=1" class="first">처음</a>
      <a href="?page={{page.previous_page_number}}" class="prev">이전</a>
  {% endif %}

  <span class="page">
      <p>{{page.number}} of {{page.paginator.num_pages}}</p> <!-- 이 부분을 작성합니다. -->
  </span>

  {% if [H] %}
      <a href="[I]" class="next">다음</a>
      <a href="[J]" class="last">마지막</a>
  {% endif %}
</div>
...
```

### 다음 페이지 구현하기
[H] 현재 페이지 다음에 페이지가 있다면 다음 페이지로 가는 링크와 마지막 페이지로 가는 링크가 나오도록 작성해 주겠습니다.

<page>.has_next를 이용해서 다음 페이지가 있는지 여부를 확인하고 쿼리스트링을 이용해서 링크를 작성합니다.

다음 페이지의 페이지 번호는 현재 페이지를 기준으로 하므로 <page>.next_page_number를 이용합니다.

마지막 페이지 번호는 paginator에 있는 전체 페이지의 개수와 같으므로 paginator의 page 개수를 나타내는 <page>.paginator.num_pages를 이용합니다.
```html
...
<div class="paging">
  {% if page.has_previous %}
      <a href="?page=1" class="first">처음</a>
      <a href="?page={{page.previous_page_number}}" class="prev">이전</a>
  {% endif %}

  <span class="page">
      <p>{{page.number}} of {{page.paginator.num_pages}}</p>
  </span>

  {% if page.has_next %} <!-- 만약 다음 페이지가 있다면 -->
      <a href="?page={{page.next_page_number}}" class="next">다음</a>
      <a href="?page={{page.paginator.num_pages}}" class="last">마지막</a>
  {% endif %}
</div>
...
```

모두 작성 되었다면 개발 서버를 켜고 일기 목록 페이지로 가서 페이지네이션이 잘 동작 하는지 확인합니다.


# Create View

1. 먼저 django.views.generic으로 부터 CreateView를 import한 후 CreateView를 상속받아 PageCreateView를 정의합니다.

```python
from django.views.generic import CreateView
...
class PageCreateView(CreateView):
```

2. PageCreateView에 필요한 클래스 변수를 작성합니다.
- model에는 여기서 사용할 모델 클래스를 지정해 주면 되는데 우리는 Page를 넣어 줍니다.
- form_class에는 마찬가지로 사용할 Form 클래스를 지정해 주면 됩니다. 우리는 PageForm을 사용합니다.
- template_name에는 랜더링할 템플릿을 적어주면 됩니다. 우리는 page_form.html을 사용합니다.

```python
from django.views.generic import CreateView
...
class PageCreateView(CreateView):
    model = Page
    form_class = PageForm
    template_name = 'diary/page_form.html'
```

3. 다음으로 정상적으로 일기 작성이 된 후 상세 보기 페이지로 이동 할 수 있도록 get_success_url 메소드를 정의합니다.
- reverse() 함수는 url 템플릿 태그와 비슷한 기능을 하는 함수로 url-name으로 이용한 실제 URL을 리턴하는 함수입니다. 이때 필요한 키워드를 kwargs 파라미터로 전달할 수 있습니다.
- 우리는 상세 보기 페이지로 이동하는데 이때 상세 보기를 할 일기를 조회할 수 있도록 page_id를 함께 넘겨 주어야 합니다.
- CreateView에서 생성된 새로운 데이터 모델은 self.object를 이용해서 접근할 수 있습니다.

```python
class PageCreateView(CreateView):
    model = Page
    form_class = PageForm
    template_name = 'diary/page_form.html'

    def get_success_url(self):
        return reverse('page-detail', kwargs={'page_id': self.object.id})
```

4. 마지막으로 urls.py로 가서 page-create가 함수형 뷰 대신 작성한 PageCreateView를 사용할 수 있도록 .as_view()를 이용해서 작성합니다.

```python
from django.urls import path
from . import views

urlpatterns = [
  ...
  path('diary/write/', views.PageCreateView.as_view(), name='page-create'),
    ...
]
```

5. views.py에 있는 기존의 page_create 함수형 뷰를 지우고 개발 서버를 실행해서 정상적으로 일기 작성이 되는지 확인해 주세요.


# List View

1. 먼저 django.views.generic으로 부터 ListView를 import한 후 ListView를 상속받아 PageListView를 구현합니다.

```python
from django.views.generic import ListView
...
class PageListView(ListView):
```

2. PageListView에 필요한 클래스 변수를 작성합니다.
- model에는 이 ListView에서 사용할 모델 클래스를 명시해 주면 됩니다. 우리는 Page입니다.
- template_name은 렌더링 할 템플릿을 적어주면 됩니다. 우리는 page_list.html을 사용합니다.
- ordering에는 정렬 기준을 적어 주면 됩니다. 생성일을 최신순으로 정렬하려면 -dt_created를 사용하면 됩니다. dt_created를 사용하게 되면 과거부터 정렬이 되기 때문에 -를 붙여서 최신순으로 정렬합니다.
- paginate_by에는 페이지네이션을 적용했을 때 한 페이지에 보여줄 데이터의 개수를 적어 주면 됩니다. 여기서는 8로 설정하겠습니다.
- page_kwarg는 쿼리 스트링으로 부터 현재 페이지에 대한 번호를 가져올 때 사용할 키워드를 적어주는 부분입니다. 이전 함수형 뷰에서 사용했던 대로 page를 사용하면 됩니다.

```python
class PageListView(ListView):
    model = Page
    template_name = 'diary/page_list.html'
    ordering = ['-dt_created']
    paginate_by = 8
    page_kwarg = 'page'
```

3. page_list 템플릿으로 가보면 지금은 뷰에서 page라는 키워드로 데이터를 넘겨주는 것을 기준으로 작성되어 있는데, generic을 이용한 ListView에서는 이 페이지의 키워드가 page_obj가 됩니다. 템플릿에 표시되어 있는 부분을 수정합니다.

```html
{% extends './base.html' %}

{% block content %}
{% if page_obj.object_list %} <!-- 수정해 주세요. -->
    <div class="wrap-note">
        <div class="note">         
            <div class="note-list">
                <ul>
                    {% for obj in page_obj.object_list %} <!-- 수정해 주세요. -->
                    <li>
                        ...
                    </li>
                    {% endfor %}
                </ul>
            </div>
            <div class="paging">
                {% if page_obj.has_previous %} <!-- 수정해 주세요. -->
                    <a href="?page=1" class="first">처음</a>
                    <a href="?page={{page.previous_page_number}}" class="prev">이전</a> <!-- 수정해 주세요. -->
                {% endif %}

                                ...

                {% if page_obj.has_next %} <!-- 수정해 주세요. -->
                    <a href="?page={{page.next_page_number}}" class="next">다음</a> <!-- 수정해 주세요. -->
                    <a href="?page={{page.paginator.num_pages}}" class="last">마지막</a> <!-- 수정해 주세요. -->
                {% endif %}
            </div>
        </div>
    </div>
{% else %}
    <div class="wrap-default">
       ...
    </div>
{% endif %}
{% endblock content %}
```

4. urls.py로 가서 page-list에 대해 함수형 뷰가 아닌 PageListView를 사용하도록 as_view() 메소드를 이용해서 작성합니다.
```python
from django.urls import path
from . import views

urlpatterns = [
    ...
    path('diary/', views.PageListView.as_view(), name='page-list'),
    ...
]
```

5. views.py에 있는 기존 page_list 함수형 뷰를 지우고 개발 서버를 실행해서 정상적으로 일기 목록 보기 페이지가 나오는지 확인해 주세요.


# Detail View

1. django.views.generic으로부터 DetailView를 import한 후 DetailView를 상속받아 PageDetailView를 정의합니다.
```python
from django.views.generic import DetailView
...
class PageDetailView(DetailView):
```

2. PageDetailView에 필요한 클래스 변수를 작성합니다.
- model에는 이 DetailView에서 사용할 모델 클래스를 명시해 주면 됩니다. 우리는 Page입니다.
- template_name은 렌더링 할 템플릿을 적어주면 됩니다. 우리는 page_detail.html을 사용합니다.
- pk_url_kwarg은 URL 패턴에 있는 데이터를 조회할 키워드의 이름을 적어주는 부분입니다. 우리는 page_id를 사용하고 있습니다.

```python
class PageDetailView(DetailView):
    model = Page
    template_name = 'diary/page_detail.html'
    pk_url_kwarg = 'page_id'
```

3. urls.py로 가서 page-detail에 대해 함수형 뷰가 아닌 PageDetailView를 사용하도록 as_view() 메소드를 이용해서 작성합니다.

```python
from django.urls import path
from . import views

urlpatterns = [
    ... 
    path('diary/page/<int:page_id>/', views.PageDetailView.as_view(), name='page-detail'),
    ...
]
```

4. views.py에 있는 기존 page_detail 함수형 뷰를 지우고 개발 서버를 실행해서 정상적으로 일기 상세보기 페이지가 나오는지 확인해 주세요.

# Update View

1. django.views.generic으로 부터 UpdateView를 Import한 후 UpdateView를 상속받아 PageUpdateView를 정의합니다.

```python
from django.views.generic import UpdateView
...
class PageUpdateView(UpdateView):
```

2. PageUpdateView에 필요한 클래스 변수를 작성합니다.
- model에는 UpdateView에서 사용할 모델 클래스를 지정해 주면 됩니다. Page를 적어 줍니다.
- 수정을 하는 일도 결국 사용자로부터 입력을 받아 서버로 전송하는 작업이므로 Form을 사용합니다. form_class에는 UpdateView에서 사용할 Form 클래스를 지정해 주면 됩니다. PageForm을 적어 줍니다.
- template_name에는 렌더링할 템플릿을 적어 주면 됩니다. 우리는 page_form.html을 사용합니다.
- 수정을 하려면 수정할 데이터를 데이터베이스에서 조회해야 하고(objects.get) 이때 조회할 조건이 필요합니다. pk_url_kwarg는 URL 패턴에 있는 데이터를 조회할 키워드의 이름을 적어주는 부분입니다. 우리는 page_id를 사용하고 있습니다.

```python
class PageUpdateView(UpdateView):
    model = Page
    form_class = PageForm
    template_name = 'diary/page_form.html'
    pk_url_kwarg = 'page_id'
```

- 다음으로 정상적으로 일기를 수정한 후 수정된 일기를 볼 수 있는 상세보기 페이지로 이동할 수 있도록 get_success_url() 메소드를 정의합니다.
    - reverse() 함수는 {url} 템플릿 태그와 비슷한 기능을 하는 함수로 url-name으로 실제 URL을 리턴하는 함수입니다. 이때 필요한 키워드를 kwargs 파라미터로 전달할 수 있습니다.
    - 우리는 상세 보기 페이지로 이동하는데 이때 상세 보기를 할 일기를 조회할 수 있도록 page_id를 함께 넘겨 주어야 합니다.

```python
class PageUpdateView(UpdateView):
    model = Page
    form_class = PageForm
    template_name = 'diary/page_form.html'
    pk_url_kwarg = 'page_id'

    def get_success_url(self):
        return reverse('page-detail', kwargs={'page_id': self.object.id})
```

3. urls.py로 가서 page-update가 함수형 뷰 대신 PageUpdateView를 사용할 수 있도록 as_view() 메소드를 이용해서 작성합니다.

```python
from django.urls import path
from . import views

urlpatterns = [
    ...
    path('diary/page/<int:page_id>/edit/', views.PageUpdateView.as_view(), name='page-update'),
    ...
]
```

views.py에 있는 기존의 page_update 함수형 뷰를 지우고 개발 서버를 실행해서 정상적으로 일기 수정이 되는지, 일기 수정이 된 후 상세 일기 보기 페이지로 이동하는지 확인해 주세요.


# Delete View 
1. django.views.generic으로 부터 DeleteView를 import한 후 DeleteView를 상속받아 PageDeleteView를 정의합니다.

```python
from django.views.generic import DeleteView
...
class PageDeleteView(DeleteView):
```

2. PageDeleteView에 필요한 클래스 변수를 작성합니다.

- model에는 DeleteView에서 사용할 모델 클래스를 지정해 주면 됩니다. 우리는 Page입니다.
- template_name에는 렌더링할 템플릿을 적어주면 됩니다. 우리는 page_confirm_delete.html을 사용합니다.
- 삭제를 하려면 삭제할 데이터를 데이터베이스에서 조회해야 하고(objects.get) 이때 조회할 조건이 필요합니다. pk_url_kwarg는 URL 패턴에 있는 데이터 조회를 위한 키워드를 적어 주는 부분입니다. 우리는 page_id를 사용하고 있습니다.

```python
class PageDeleteView(DeleteView):
    model = Page
    template_name = 'diary/page_confirm_delete.html'
    pk_url_kwarg = 'page_id'
```

- 정상적으로 일기를 삭제한 후 이동할 페이지의 URL을 get_success_url() 메소드를 통해 명시합니다.

  - reverse() 함수는 {url} 템플릿 태그와 비슷한 기능을 하는 함수로 url-name으로 실제 URL을 리턴하는 함수입니다.
  - 우리는 삭제한 다음 일기 목록 보기 페이지로 안내합니다.

```python
class PageDeleteView(DeleteView):
    model = Page
    template_name = 'diary/page_confirm_delete.html'
    pk_url_kwarg = 'page_id'

    def get_success_url(self):
        return reverse('page-list')
```

3. urls.py로 가서 page_delete가 함수형 뷰 대신 PageDeleteView를 사용할 수 있도록 as_view() 메소드를 이용해서 작성합니다.

```python
from django.urls import path
from . import views

urlpatterns = [
     ...
    path('diary/page/<int:page_id>/delete/', views.PageDeleteView.as_view(), name='page-delete'),
]
```

4. views.py에 있는 기존의 page_delete 함수형 뷰를 지우고 개발 서버를 실행해서 정상적으로 일기가 삭제되는지 확인해 주세요.

# Generic View 정리하기
Django에서 제공하는 제네릭 뷰는 역할에 따라 크게 네 가지로 나누어져 있습니다. 우리는 각각 로직에 맞는 기능을 편하게 구현할 수 있게 하는 클래스 변수와 메소드를 이용해서 정해진 틀에 따라 구현을 해야 하는데 처음에는 이런 부분들이 조금 생소하게 느껴질 수 있지만 필요할 때마다 하나씩 사용하다 보면 금방 익숙해지실 거에요.

|종류|	뷰	|설명|
|---|----|---|
|Base Views	| TemplateView RedirectView	|템플릿을 랜더해서 결과로 돌려주거나 다른 URL로 리디렉션 하는등의 기본적인 기능을 하는 뷰|
|Display Views|	ListView DetailView	|데이터를 보여주는 기능을 하는 뷰|
|Edit Views|	FormView CreateView UpdateView DeleteView	|데이터 생성, 수정, 삭제등의 기능을 하는 뷰|
|Date Views	|YearArchiveView MonthArchiveView DayArchiveView TodayArchiveView	|날짜를 중심으로 데이터를 조회하는 기능을 하는 뷰|

Date Views 링크  
https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-date-based/

아래는 우리가 강의에서 함께 구현해 보았던 제네릭 뷰의 각 속성들을 정리해놓은 것 입니다. 내가 구현하려하는 뷰가 CRUD 로직에 해당하는 뷰라면 제네릭뷰 사용을 꼭 고려해 보세요.

## Base Views
Base Views 문서 바로가기  
https://docs.djangoproject.com/en/2.2/ref/class-based-views/base/

### RedirectView
RedirectView는 들어온 요청을 새로운 URL로 이동시키는 기능을 합니다.

| 속성|	설명	|기본값 |
|----|---|----|
| url|	이동할 URL을 지정하는 속성	|None|
| pattern_name	|URL 패턴의 이름을 지정하는 속성|	None|
| query_string	|쿼리 스트링을 전달할 지 여부	|False|

### TemplateView
TemplateView는 주어진 템플릿을 렌더링해서 보여주는 기능을 합니다.
|속성	설명	기본값
|template_name	렌더할 템플릿을 지정하는 속성	None|

## Display Views
Display Views 문서 바로가기  
https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/


### DetailView
DetailView는 하나의 데이터를 보여주는 기능을 합니다. 우리가 같이해봤던 '상세 보기'를 생각하면 됩니다.

|속성|	설명	|기본값|
|---|---|---|
|model|	사용할 모델 지정	|None|
|pk_url_kwarg	|보여주기 위한 단일 데이터를 조회할 때 사용할 키워드 인수 지정 (urls.py에서 지정한 키워드 인수)|	'pk'|
|template_name	|렌더할 템플릿을 지정하는 속성|	None|
|context_object_name	|템플릿으로 전달할 모델의 context 키워드 지정	|'<model_name>'|

### ListView
ListView는 여러 데이터를 보여주는 기능을 합니다. 우리가 같이해봤던 '목록 보기'를 생각하면 됩니다.

|속성	|설명	|기본값|
|model	|사용할 모델 지정	|None|
|ordering	|데이터 정렬 속성 지정(order_by와 동일한 값 사용)|	None|
|paginate_by	|페이지에 표시 할 데이터의 수	|None|
|page_kwarg|	쿼리스트링으로부터 가져올 현재 페이지에 대한 키워드|	‘page’|
|template_name|	렌더할 템플릿을 지정하는 속성|	None|
|context_object_name|	템플릿으로 전달할 모델의 context 키워드 지정|	'<model_name>_list'|

## Editing Views
Editing Views 문서 바로가기
https://docs.djangoproject.com/en/4.1/

### FormView
FormView는 Form을 렌더링해서 보여주는 기능을 하는 뷰입니다.

|속성	|설명	|기본값|
|---|---|---|
|form_class	|입력을 위한 Form Class를 지정합니다.|	None|
|success_url|	처리가 성공했을 때 리디렉션 할 URL을 지정	|None|
|template_name|	렌더할 템플릿을 지정하는 속성|	None|

### CreateView
Createview는 새로운 데이터를 생성을 위한 뷰입니다.

|속성|	설명	|기본값|
|---|---|---|
|model	사용할 모델 지정|	None|
|form_class	|입력을 위한 Form Class를 지정합니다.	|None|
|fields|	데이터 입력에 사용할 필드를 명시적으로 지정합니다.|	None|
|template_name	|렌더할 템플릿을 지정하는 속성|	None|
|pk_url_kwarg	|보여주기 위한 단일 데이터를 조회할 때 사용할 키워드 인수 지정 urls.py에서 지정한 키워드 인수)|	'pk'|
|success_url	|처리가 성공했을 때 리디렉션 할 URL을 지정	|None|

### UpdateView
UpdateView는 기존 데이터 개체의 수정을 위한 뷰입니다.

|속성	|설명	|기본값|
|---|---|---|
|model|	사용할 모델 지정|	None|
|form_class|	입력을 위한 Form Class를 지정합니다.|	None|
|field	|데이터 입력에 사용할 필드를 명시적으로 지정합니다.	|None|
|template_name	|렌더할 템플릿을 지정하는 속성	|None|
|pk_url_kwarg	|보여주기 위한 단일 데이터를 조회할 때 사용할 키워드 인수 지정 (urls.py에서 지정한 키워드 인수)|	‘pk’|
|success_url	|처리가 성공했을 때 리디렉션 할 URL을 지정	|None|
|context_object_name	|템플릿으로 전달할 모델의 context 키워드 지정	|<model_name>|

### DeleteView
DeleteView는 기존 데이터를 삭제하는 기능을 위한 뷰입니다.

|속성	|설명	|기본값|
|---|---|----|
|model|	사용할 모델 지정	|None|
|template_name	|렌더할 템플릿을 지정하는 속성|	None|
|pk_url_kwarg|	보여주기 위한 단일 데이터를 조회할 때 사용할 키워드 인수 지정 (urls.py에서 지정한 키워드 인수)|	‘pk’|
|success_url|	처리가 성공했을 때 리디렉션 할 URL을 지정	|None|
|context_object_name|	템플릿으로 전달할 모델의 context 키워드 지정	|<model_name>|

## Context 정리하기
Context는 View에서 Template으로 전달되어 렌더링시 사용할 수 있는 사전형 데이터 변수입니다. 앞에서 함수형 뷰를 사용할 때 render 함수의 세 번째 파라미터로 넘겨서 사용했었죠.

```python
def function_view(request):
    return render(request, template_name, context)
```

Django의 Generic 뷰는 이러한 Context를 각각의 기능에 맞게 자동으로 Template에 전달합니다. 헷갈릴 수 있는 부분이니까 우리가 사용했던 CRUD를 중심으로 정리해보겠습니다.

### 모델(Model) 데이터
기본적으로 모델(Model) 데이터는 Template에 context로 전달됩니다. 하나의 데이터를 다루는 View는 하나의 데이터를 'object'라는 키워드로 전달하고 여러개의 데이터를 다루는 View는 'object_list'라는 키워드로 전달합니다. 그리고 같은 데이터를 'model' 클래스 변수에 명시한 Model을 보고 소문자로 변형해 함께 전달합니다. 아래 예시를 보면서 이해해봅시다.

```python
from django.views.generic import DetailView
from .models import Post
    
class PostDetailView(DetailView):
    model = Post
    ...
```

DetailView는 하나의 데이터를 다루는 로직을 수행합니다. 그래서 위처럼 model 클래스 변수를 지정하면 자동으로 ‘object’라는 키워드로 데이터베이스에서 조회한 하나의 Post 데이터를 Template에 전달합니다. 그러면 Template에서는 템플릿 변수를 사용해서 {{object.title}} 같은 형태로 접근할 수 있는거죠. 그리고 이 object와 똑같은 데이터를 모델명을 소문자로 쓴 형태인 post로도 Template에 함께 전달합니다. 그러니까 같은 데이터가 object와 post 두 개의 키워드로 전달되는거죠. 이렇게 되면 우리는 Template에서 조금 더 직관적인 {{post.title}} 같은 형태로 사용할 수 있습니다.

```python
from django.views.generic import ListView
from .models import Post
    
class PostListView(ListView):
    model = Post
    ...
```

자, 이번에는 ListView를 예로 들어볼게요. ListView는 여러 데이터를 다루는 로직을 수행하죠? 그래서 model 클래스 변수를 지정하면 자동으로 데이터베이스에서 조회한 Post 데이터 목록을 object_list라는 키워드로 Template에 전달합니다. 그리고 이때 똑같은 데이터를 model 키워드 변수에 명시된 모델을 참고하여 소문자로 쓴 형태인 <model_name>_list 즉 post_list 키워드로도 context를 전달합니다. 그러니까 Template에서는 object_list와 post_list 두 개의 키워드로 Post 데이터 목록에 접근할 수 있는겁니다.

### context_obejct_name
자, 그러면 context_object_name 클래스 변수는 무엇을 지정해주는 걸까요? 위에서 설명한 context 중 바로 모델명을 보고 유추하는 <model_name> 또는 <model_name>_list 같은 이름들을 바꿔주는 것 입니다. Django가 알아서 모델명을 보고 유추해서 넘겨주는 context 이름을 커스터마이징 할 수 있는거죠. 이것도 예시를 보면서 이해해봅시다.

```python
from django.views.generic import ListView
from .models import Post
    
class PostListView(ListView):
    model = Post
     ...
```

이렇게 적으면 Post 데이터 목록이 object_list와 post_list라는 두 개의 키워드로 전달되겠죠? 그런데 이때 context_object_name을 아래와 같이 명시해주면

```python
from django.views.generic import ListView
from .models import Post
    
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ...
```

post_list 가 posts로 변경되어 전달됩니다. 그러니까 Post 데이터목록이 object_list와 posts 두 개의 키워드로 전달되게 되는거죠. 이렇게 generic 뷰가 자동으로 모델을 보고 생성하는 context 키워드를 변경해 주는 것이 바로 context_object_name 입니다.

# 그 외 Context 목록
위에서 설명한 context 말고도 우리가 함께 사용해보았던 context도 있습니다. 당연히 이러한 context를 모두 외울 필요는 없고 '아, 그런것도 있었는데?' 정도의 경험을 갖는 것이 중요합니다. 실제 어떻게 구현해야하는지 형태가 무엇인지는 필요할 때 Django 공식 문서를 보고 찾아서 구현하면 됩니다.

### CreateView

| 키워드	                                   | 설명                                |
|----------------------------------------|-----------------------------------|
| form | 	form_class 클래스 변수에 명시한 폼이 전달됩니다. |

### ListView

|키워드	|설명|
|---|---|
|paginator	|Paginator 객체가 전달됩니다.|
|page_obj	|현재 Page 객체가 전달됩니다.|
|is_paginated	|페이지네이션 적용 여부가 boolean 형으로 전달됩니다.|

### UpdateView
|키워드	|설명|
|---|---|
|form	|form_class 클래스 변수에 명시한 폼이 전달됩니다.|

