from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):
    """
    Dozvoljava pristup samo vlasniku objekta ili admin korisniku.
    """
    def has_object_permission(self, request, view, obj):
        # Admin ili superuser ima sva prava
        if request.user.is_superuser or request.user.groups.filter(name="AdminGroup").exists():
            return True
        # Provera da li je korisnik vlasnik objekta
        return obj.user == request.user


class IsLocationOwnerOrAdmin(BasePermission):
    """
    Permission class that allows access only to the owner of a Location (or related objects)
    or to admin users.

    Works with Location, LocationImages, LocationWorkingHours and similar objects.
    """
    def has_object_permission(self, request, view, obj):
        user = getattr(request, 'user', None)
        if not user or user.is_anonymous:
            return False

        # Admins always allowed
        if user.is_superuser or user.groups.filter(name="AdminGroup").exists():
            return True

        # If object is a Location instance
        if hasattr(obj, 'customer') and getattr(obj, 'customer') is not None:
            customer = obj.customer
            # customer.owner or customer.user may point to the owning user
            owner = getattr(customer, 'owner', None)
            cust_user = getattr(customer, 'user', None)
            return owner == user or cust_user == user

        # If object is related to a Location (e.g., LocationImages, LocationWorkingHours)
        if hasattr(obj, 'location') and getattr(obj, 'location') is not None:
            customer = getattr(obj.location, 'customer', None)
            if customer:
                owner = getattr(customer, 'owner', None)
                cust_user = getattr(customer, 'user', None)
                return owner == user or cust_user == user

        # Fallback: if object has a 'user' attribute match against it
        if hasattr(obj, 'user'):
            return getattr(obj, 'user') == user

        return False
