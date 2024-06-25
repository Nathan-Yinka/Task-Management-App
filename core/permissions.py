from rest_framework import permissions

class IsAssignedOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            print("fmfmfnmnfnnfnfnfnfnnfnfnfnnf")
            return True
        
        if not request.user.is_authenticated:
            return False
        
        return obj.assigned_to == request.user
        