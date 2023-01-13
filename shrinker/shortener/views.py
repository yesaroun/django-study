from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shortener.models import Users
from django.shortcuts import render, redirect


def index(request):
    user = Users.objects.filter(username="admin").first()
    email = user.email if user else "Anonymous User"
    return render(request, "base.html", {"welcome_msg":f"Hello {email}", "hello": "world"})

@csrf_exempt
# csrf토큰으로 요청을 위변조 하는 것을 방지한다.
# csrf_exempt : csrf 토큰을 하지말라는 뜻 왜 하지말라고 했냐면 postman으로 테스트 해보기 위해서
def get_user(request, user_id):
    print(user_id)
    # request.method가 POST인 경우와 GET인 경우 분기
    if request.method == "GET":
        abc = request.GET.get("abc")
        xyz = request.GET.get("xyz")
        user = Users.objects.filter(pk=user_id).first()
        return render(request, "base.html", {"user": user, "params": [abc, xyz]})
        # http://127.0.0.1:8000/get_user/1?abc=123&xyz=abc
        # 이렇게 쿼리스트링을 보낼 수 있다.
    elif request.method == "POST":
        username = request.GET.get("username")
        if username:
            user = Users.objects.filter(pk=user_id).update(username=username)

        # return JsonResponse(dict(msg="You just reached with Post Method!"), safe=False)
        # json이 한글일 경우 safe=False 하면 깨지지 않는다.
        return JsonResponse(status=201, data=dict(msg="You just reached with Post Method!"), safe=False)
        # status를 하면 뒤에 data= 이 형태로 수정해야함
        # status 정하면 postman에서 status: 201로 변함
