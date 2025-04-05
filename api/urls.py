from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register(r'customers', CustomerViewSet, basename='customers')


urlpatterns = router.urls + [
    #path('', api_view, name='api'),
]
