## 목차
- [REST API](#rest-api)
  - [Wishlist API](#wishlist-api)
    - [WishlistDetail](#class-wishlistdetail)
    - [WishlistToggle](#class-wishlisttoggle)
    - [좋아요 기능(RoomDetailSerializer.get_is_liked)](#좋아요-기능)

## REST API
### Wishlist API

#### class WishlistDetail
> wishlists/views.py WishlistDetail

[source code](wishlists/views.py)

<br>

```python
    permission_classes = [IsAuthenticated]
```
인증 받지 않으면 진행할 수 없도록 처리

```python
    def get_object(self, pk: int, user: User) -> WishList:
        try:
            return WishList.objects.get(pk=pk, user=user)
        except WishList.DoesNotExist:
            raise NotFound
```
WishList는 private 하기 때문에 유저만 볼 수 있다. 그래서 url로 요청하는 user도 받아온다.

```python
    def put(self, request: Request, pk: int) -> Response:
        wishlist: WishList = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,           # database에서 온 wishlist
            data=request.data,  # user data
            partial=True,       # 부분적 update True
        )
        if serializer.is_valid():
            wishlist = serializer.save()        # updated된 wishlist 반환
            serializer = WishlistSerializer(
                wishlist,
                context={"request": request},   # 
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
```

#### class WishlistToggle
> wishlists/views.py WishlistToggle 클래스

[source code](wishlists/views.py)

<br>


```python
    def put(self, request: Request, pk: int, room_pk: int) -> Response:
        wishlist: WishList = self.get_list(pk, request.user)
        room: Room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room.pk).exists():  # 해당 값이 존재하는지 여부 확인
        # wishlist.rooms.filter(pk=room.pk) -> 이건 해당하는 list 반환
            wishlist.rooms.remove(room) # 방이 있다면 삭제
        else:                           # 그렇지 않다면 wishlist에 room을 넣고 싶은 거임
            wishlist.rooms.add(room)
        return Response(status=status.HTTP_200_OK)
```


#### 좋아요 기능
> rooms/serializer.py RoomDetailSerializer

[source code](rooms/serializers.py)

```python
class RoomDetailSerializer(ModelSerializer):
    """
    Room detail을 위한 Serailizer
    """
        
    # 중략
    
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()      # 추가
    photos = PhotoSerializer(many=True, read_only=True)
    
    # 중략

    def get_is_liked(self, room) -> bool:               # 추가
        """
        유저가 Room 인스턴스에 좋아요를 눌렀는지 확인
        """
        request = self.context["request"]           # 어떤 user가 이 방을 보고 있는지 확인하기 위해
        return WishList.objects.filter(             # request.user가 갖고 있는 wishlist들을 찾아와야 한다. 1)
            user=request.user,
            rooms__pk=room.pk,                      # 2)
        ).exists()                                  # true or false 결과 값을 필요로 하기 때문
```
1 ) 에서 get 대신 filter를 쓴 이유는 유저가 여러 개의 wishlist를 가지고 있을 수 있기 때문
정리하면 우선 room을 보고 있는 user가 소유한 wishilst들을 찾고, wishlist를 한번 더 filter 하는데 room list에 그 room을 가지고 있는 wishlist를 찾아내야 한다. 이 두 번째 과정은 2)에서 한다.

2 ) user가 만든 wishlist중에 room id(pk)가 있는 room list를 포함한 wishlist를 찾아 pk랑 room pk가 일치하는 room을 가져다 준다.  
-> [관련 장고 문서](https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_many/)  
이 코드는 아래처럼 room name이 'apt. seoul'인 room이 있는 wishlist도 찾을 수 있다.
```python
    def get_is_liked(self, room) -> bool:
        request = self.context["request"]
        return WishList.objects.filter(
            user=request.user,
            rooms__name="apt. seoul",
        ).exists()
```


