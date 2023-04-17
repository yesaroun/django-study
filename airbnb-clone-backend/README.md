## 목차
- [REST API](#rest-api)
  - [Wishlist API](#wishlist-api)
    - [WishlistDetail](#class-wishlistdetail)
    - [WishlistToggle](#class-wishlisttoggle)
    - [좋아요 기능(RoomDetailSerializer.get_is_liked)](#좋아요-기능)
  - [Booking](#booking-api)
    - [RoomBookings-GET](#class-roombookings-get)
    - [RoomBooking-POST](#class-roombookings-post)
  

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

### Booking API

#### class RoomBookings (get)
url : /rooms/<int:pk>/bookings

[rooms.views.py RoomBookings](./rooms/views.py)

```python
    permission_classes = [IsAuthenticatedOrReadOnly]
```
로그인 한 유저만 room 예약하도록 처리  
그래서, get은 허용하지만 그 외는 허용하지 못하도록 처리

```python 
    def get_object(self, pk) -> Room:
        """
        pk에 맞는 Room 객체 반환
        """
        
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFoud

    def get(self, request, pk) -> Response:
        """
        pk에 해당하는 Room 객체 get
        """
        
        room: Room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()     # 2)
        bookings = Booking.objects.filter(                  # 1)
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,                               # 3)
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)
```
##### 1)
```python
bookings = Booking.objects.filter(room__pk=pk)
```
이렇게 get_object method를 사용하지 않고도 가능하다.  
이러면, DB를 두 번 조회하지 않는다.

다만, 이 경우 booking이 없을 경우와 room이 존재하지 않을 경우 모두 빈 리스트를 출력한다.  
그래서 user가 방 자체가 없는 상황에도 예약이 되지 않았다고 생각할 것이다.  

##### timezone 관련)  
booking 했을 때 check_out 날짜가 check_in 날짜보다 더 미래여야 한다.  
그래서
```python
from django.utils import timezone
```
이렇게 import 한다. django에서 시간을 알아내고 싶거나, timezone 관련 작업을 하면 파이썬 내장 datetime 모듈보다는 django의 timezone을 사용하는게 좋다.  
왜냐하면 django timezone 관련 작업할 때 유용한 것들 제공할 것임(서버의 로컬 타임 등등)

django timezone을 사용하려면 config/settings.py에서 
```python
USE_TZ = True
```
이렇게 timezone을 작업한다고 한다.(기본으로 세팅 되어 있음)  
또한, 
```python
TIME_ZONE = "Asia/Seoul"
```
이렇게 서버의 로컬 타임도 지정할 수 있다.

##### 2)
```python
now = timezone.now()
print(now)                          # 2023-04-12 04:02:39.303022+00:00
print(timezone.localtime(now))      # 2023-04-12 13:03:58.798155+09:00
```
이렇게 로컬 타임으로 출력 가능
```python
now = timezone.localtime(timezone.now()).date()
```
.date() 메소드를 이용해서 date(날짜)만 사용

##### 3)
```python
check_in__gt=now,
```
check_in이 greater than now 해야 한다.  

정리하면 우리 서버가 있는 위치의 현지 시각을 localtime을 이용해 구하고 check_in 날짜가 현재 날짜보다 큰 booking을 찾고 있다.


#### class RoomBookings (post)

[rooms.views.py RoomBookings](./rooms/views.py)

```python
    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(data=request.data)     # 1)
        if serializer.is_valid():                                       # 2)
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
```

##### 1)
User가 데이터를 보내면 Serializer가 model의 요구조건에 맞춰서 data를 검증

##### 2)
user가 check_in, out에 보내는 date 값이 미래의 날짜어야 한다. 그래서 serizlizer.is_valid()만으로는 부족하다. 다른 validation을 만들어야 한다.  
그 validation은 serializer에서 작성


```python
class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()         # 3)

    class Meta:
      # 중략

    # 4) 
    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()     # 5)
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate(self, data):
        # validation 1 : check_in 날짜가 check_out보다 클 경
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check in should be smaller than check out."
            )
        # validation2 : booking을 저장하기 전에 이 날짜 사이에 다른 booking이 있는지 확인
        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
            # 이 경우는 이미 예약이 존재하니까 user가 예약을 할 수 없다고 알려야 한다
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of those dates are already taken."
            )
        return data
```

##### 3)
여기서는 날짜 필드가 맞는지 체크한다. 여기에서 검증하는 결과에 따라 view의 valid가 동작하는 것이다. 추가적인 검증이 필요하다면 아래에서 반영할 수 있다.

##### 4)
validate 뒤에 _ 를 입력하고 validate 하고 싶은 field의 이름을 입력한다. 예: check_in

##### 5)
오늘 date만 받아옴

