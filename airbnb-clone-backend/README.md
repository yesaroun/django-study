## 목차
- [REST API](#rest-api)
  - [Wishlist API](#wishlist-api)
    - [WishlistDetail](#class-wishlistdetail)
    - [WishlistToggle](#class-wishlisttoggle)

## REST API
### Wishlist API

#### class WishlistDetail
> wishlists/views.py WishlistDetail 클래스 전문
```python
class WishlistsDetail(APIView):
    """
    단일 wishlist 객체 View
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk: int, user: User) -> WishList:
        """
        pk와 user에 해당하는 Wishlist 객체 반환

        :param pk: 검색할 Wishlist 객체의 pk
        :param user: Wishlist 객체와 연결된 user
        :return: Wishlist 객체
        :raise: 객체가 존재하지 않으면 NotFound
        """
        try:
            return WishList.objects.get(pk=pk, user=user)
        except WishList.DoesNotExist:
            raise NotFound

    def get(self, request: Request, pk: int) -> Response:
        """
        pk와 user에 해당하는 Wishlist 객체 get

        :param request: HTTP request object
        :param pk: 검색할 WishList 객체의 pk
        :return: serialized Wishlist object data
        """
        wishlist: WishList = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request: Request, pk: int) -> Response:
        """
        pk와 user에 해당하는 Wishlist 객체 삭제

        :param request: HTTP request object
        :param pk: 삭제할 WishList 객체의 pk
        :return: HTTP status code
        """
        wishlist: WishList = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        """
        pk와 user에 해당하는 Wishlist 객체 update

        :param request: HTTP request object
        :param pk: 업데이트할 Wishlist 객체의 pk
        :return: 업데이트된 Wishlist 객체 또는 error 메세지
        """
        wishlist: WishList = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(
                wishlist,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
```

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
> wishlists/views.py WishlistToggle 클래스 전문

```python
class WishlistToggle(APIView):
    """
    user의 wishlist toggle을 위한 APIView
    """

    def get_list(self, pk: int, user: User) -> WishList:
        """
        pk와 user에 해당하는 WishList 객체 반환

        :param pk: 검색할 WishList 객체의 pk
        :param user: Wishlist 객체와 연결된 user
        :return: Wishlist 객체
        :raise: 객체가 존재하지 않으면 NotFound
        """
        try:
            return WishList.objects.get(pk=pk, user=user)
        except WishList.DoesNotExist:
            raise NotFound

    def get_room(self, pk: int) -> Room:
        """
        pk에 해당하는 Room 객체 반환

        :param pk: 검색할 Room 객체의 pk
        :return: Room 객체
        :raise: 존재하지 않으면 NotFound
        """
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, request: Request, pk: int, room_pk: int) -> Response:
        """

        :param request: HTTP Request object
        :param pk: Wishlist 객체의 pk
        :param room_pk: Room 객체의 pk
        :return:
        """
        wishlist: WishList = self.get_list(pk, request.user)
        room: Room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=status.HTTP_200_OK)
```

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