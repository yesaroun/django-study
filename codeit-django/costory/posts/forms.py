from django import forms
from .models import Post
from .validators import validate_symbols
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    # memo = forms.CharField(max_length=80, validators=[validate_symbols])
    # 이렇게 필드를 정의할때 유효성 검사를 할 수 있다.

    class Meta:
        model = Post
        fields = ["title", "content"]

    # 다른 방식
    def clean_title(self):
        title = self.cleaned_data["title"]
        # 모든 Form 클래스는 기본적으로 cleaned_data를 가지고 있는데
        # cleaned_data 안에는 폼 필드를 정의할 때 넣어준 유효성 검사를 통과한 데이터가 있다
        # 만약 폼 필드 사용하지 않으면 유저가 입력한 데이터가 그대로 넘어온다
        # 지금은 모델 필드에 유효성을 넣었으니까 여기서 가져온 cleaned_data['title']에는 유효성 검증이 이루어지지 않았다.
        # 그래서 title에 유효성 검증을 추가하면 된다. 아래처럼
        if "*" in title:
            raise ValidationError("*는 포함될 수 없습니다.")

        return title

    # 이렇게 clean_filed 형식은 하나의 필드에 대해서만 검증이 가능하며 유효성 검증 에러를 내는 것과는 관계없이 항상 이런 return title 을 해서
    # cleand_datad에서 가져온 데이터를 항상 리턴
    # 반면에 Validator는 한번 정의하면 모델과 폼에서 모듀 사용 가능하고 여러 필드에서 사용 가능하다.
