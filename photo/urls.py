from django.urls import path
from .views import PhotoList, PhotoDelete, PhotoDetail, PhotoUpdate, PhotoCreate, PhotoLike, Photofavorite, PhotoLikeList, PhotoFavoriteList, PhotoMyList, comment_create_photo, comment_modify_photo, comment_delete_photo
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "photo"
urlpatterns = [
    path("mylist/", PhotoMyList.as_view(), name="mylist"),
    path("create/", PhotoCreate.as_view(), name='create'),
    path("like/<int:photo_id>/", PhotoLike.as_view(), name='like'),
    path("favorite/<int:photo_id>/", Photofavorite.as_view(), name='favorite'),
    path("delete/<int:pk>/", PhotoDelete.as_view(), name='delete'),
    path("update/<int:pk>/", PhotoUpdate.as_view(), name='update'),
    path("detail/<int:pk>/", PhotoDetail.as_view(), name='detail'),
    path("like/", PhotoLikeList.as_view(), name="like_list"),
    path("favorite/", PhotoFavoriteList.as_view(), name="favorite_list"),
    path('detail/<int:photo_id>/comment_create/', views.comment_create_photo, name='comment_create'),
    path('detail/<int:comment_id>/comment_modify/', views.comment_modify_photo, name='comment_modify'),
    path('detail/<int:comment_id>/comment_delete/', views.comment_delete_photo, name='comment_delete'),
    path('', PhotoList.as_view(), name='index'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)