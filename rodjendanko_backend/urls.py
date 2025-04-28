"""
URL configuration for rodjendanko_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt import views as jwt_views
from django.contrib.auth import views as auth_views
from api.views.v_user import CustomTokenObtainPairView
from api.views.v_customer_registration import CustomerRegistrationView


schema_view = get_schema_view(
    openapi.Info(
        title="Rodjendarijum API",
        default_version='v1',
        description="API Dokumentacija za Rodjendarijum",
        terms_of_service="https://rodjendarijum.lenitech.org",
        contact=openapi.Contact(email="admin@rodjendarijum.lenitech.org"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/', include('api.urls')),
    path('', include('users.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('auth/social/', include('allauth.socialaccount.urls'))
]
