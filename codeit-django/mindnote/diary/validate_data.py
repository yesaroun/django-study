from .models import Page
import random


def validate_pages():
    pages = Page.objects.all()
    for page in pages:
        if page.score < 0 or page.score > 10:
            page.score = random.randint(0, 10)  # 0~10 사이의 무작위 정수로 수정
            page.save()
