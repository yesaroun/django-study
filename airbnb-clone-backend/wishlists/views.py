from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import WishList
from rooms.models import Room
from django.contrib.auth.models import User
from .serializers import WishlistSerializer


class WishLists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlists = WishList.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            all_wishlists,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(
                user=request.user,
            )
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


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
            partial=True,  # 부분적 update True
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
