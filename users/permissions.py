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
