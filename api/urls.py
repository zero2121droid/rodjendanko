from django.urls import path
from django.urls import include
from api.views.v_user import UserViewSet, ChildrenViewSet
from rest_framework.routers import DefaultRouter
from api.views.v_customer import CustomerViewSet
from api.views.v_services import CustomerServicesViewSet, PartnerServicesViewSet, OtherServicesViewSet, ServicesImagesViewSet
from api.views.v_bookings import BookingsViewSet
from api.views.v_location import LocationViewSet, LocationImagesViewSet, LocationWorkingHoursViewSet
from api.views.v_notifications import NotificationViewSet
from api.views.v_wallet import WalletViewSet, WalletTransactionViewSet
from api.views.v_user_registration import UserRegistrationView
from api.views.v_customer import CustomerViewSet
from api.views.v_customer_registration import CustomerRegistrationView


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='users')
router.register(r'children', ChildrenViewSet, basename='children')
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'customer-services', CustomerServicesViewSet, basename='customer-services')
router.register(r'partner-services', PartnerServicesViewSet, basename='partner-services')
router.register(r'other-services', OtherServicesViewSet, basename='other-services')
router.register(r'services-images', ServicesImagesViewSet, basename='services-images')
router.register(r'bookings', BookingsViewSet, basename='bookings')
router.register(r'location', LocationViewSet, basename='location')
router.register(r'location-images', LocationImagesViewSet, basename='location-images')
router.register(r'location-working-hours', LocationWorkingHoursViewSet, basename='location-working-hours')
router.register(r'wallet', WalletViewSet, basename='wallet')
router.register(r'wallet-transactions', WalletTransactionViewSet, basename='wallet-transactions')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = router.urls + [
    path('customer/register/', CustomerRegistrationView.as_view(), name='customer-register'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
