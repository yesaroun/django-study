from rest_framework.serializers import ModelSerializer
from .models import Feed
from users.serializers import FeedUserSerializer
from reviews.serializers import FeedReviewsSerializer

# (1) 전체 데이터를 다 보여주는 Serialize
class FeedSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = "__all__"
        depth = 1 # objects도 serialize화 시킴

# (2) 일부 데이터만 보여주는 Serialize
class FeedListSerializer(ModelSerializer):
    user = FeedUserSerializer()

    class Meta:
        model = Feed
        fields = ("id", "content", "like", "user")

# (3) 하나의 Feed만 보여주는 Serialize
class FeedDetailSerializer(ModelSerializer):
    user = FeedUserSerializer(read_only=True) # 유저한테서 유저정보를 입력받으면 안됨.
    review_set = FeedReviewsSerializer(many=True, read_only=True)

    class Meta:
        model = Feed
        fields = "__all__"

# feed = Feed.objects.get(id=1)
# feed.user
# feed.review_set
