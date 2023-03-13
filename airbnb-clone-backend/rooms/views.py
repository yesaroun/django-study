from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(
        request,
        "rooms/all_rooms.html",
        {
            "rooms": rooms,
            "title": "hello! ",
        },
    )


def see_one_room(request, room_id):
    return HttpResponse(f"see room with id: {room_id}")
