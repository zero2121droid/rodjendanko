from django.urls import path
from api.views.v_user import UserViewSet, ChildrenViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='users')
router.register(r'children', ChildrenViewSet, basename='children')

urlpatterns = router.urls 
