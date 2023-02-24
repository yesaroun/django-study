from django.urls import path
from . import views

urlpatterns = [
    path("diary/", views.page_list, name="page-list"),
    path("diary/info", views.info, name="info"),
    path("diary/write", views.page_create, name="page-create"),
    path("diary/page/<int:page_id>", views.page_detail, name="page-detail"),
    path("diary/page/<int:page_id>/edit", views.page_update, name="page-update"),
    # path('diary/page/<int:page_id>/delete', views.page_delete, name='page-delete),
]
