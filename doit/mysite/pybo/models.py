from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)  # 글자 수 제한하고 싶은 경우 CharField()
    content = models.TextField()                # 글자 수 제한이 없는 경우 TextField()
    create_date = models.DateTimeField()        # 날짜, 시간 관련 속성
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # ForeingKey : ForeingKey 지정
    # on_delete=models.CASCADE : 답변에 연결된 질문이 삭제되면 답변도 함께 삭제하라는 의미
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
