from django.contrib import admin
from django.urls import path
from rareapi.views import register_user, login_user, is_admin

from rareapi.views import RareUserView, TagView, CategoryView, CommentView

from rest_framework import routers
from django.conf.urls import include
from rareapi.views import PostView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostView, 'post')
router.register(r'tags', TagView, "tags")
router.register(r'users', RareUserView, 'user')
router.register(r'comments', CommentView, 'comment')
router.register(r'categories', CategoryView, 'category')
router.register(r'users', RareUserView, 'user')

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin', is_admin)
]
