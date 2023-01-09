from django.shortcuts import render
from django.http import HttpResponse

# def show_feed(request):
# 	return HttpResponse("show feed")

# def one_feed(request, feed_id):
# 	return HttpResponse(f"feed id: {feed_id}, {feed_content}")
# 	try:
# 		feed = Feed.objects.get(id=feed_id)
# 		return render(request, "feed.html", {"feed":feed})
# 	except Feed.DoesNotExist:
# 		return render(request, "feed.html", {"error":True})

# def all_feed(request):
# 	feeds = Feed.objects.all()
# 	# return HttpResponse("all feed")
# 	# return render(request, "feeds.html")
# 	return render(request, "feeds.html", {"feeds":feeds, "content":"내용"})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated

from .models import Feed
from .serializers import FeedSerializer, FeedListSerializer, FeedDetailSerializer

class Feeds(APIView):
	def get(self, request):
		feeds = Feed.objects.all()
		# serializer = FeedSerializer(feeds, many=True)
		serializer = FeedListSerializer(feeds, many=True)
		return Response(serializer.data)

	def post(self, request):
		if request.user.is_authenticated:
			# request.data => 유저로 부터 입력받은 데이터
			serializer = FeedDetailSerializer(data=request.data)
			
			# JSONT => Serialize한 데이터를 Feed Moels을 기반으로 data validation
			if serializer.is_valid():			
				# save()함수가 정상실행되면 => serializer의 create() 함수 실행됨
				# request를 날린 유저의 데이터를 Feed에 저장
				feed = serializer.save(user=request.user)
				serializer = FeedDetailSerializer(feed)
				return Response(serializer.data)
			else:
				return Response(serializer.errors)
		else:
			raise NotAuthenticated

class FeedDetail(APIView):
	def get_object(self, feed_id):
		try:
			return Feed.objects.get(id=feed_id)
		except Feed.DoesNotExist:
			raise NotFound

	def get(self, request, feed_id):
		feed = self.get_object(feed_id)
		serializer = FeedDetailSerializer(feed)
		return Response(serializer.data)
