from rest_framework.permissions import BasePermission

# GMS Imports


class OwnerOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return "Owner" in request.user["roles"]


class OwnerAndSupervisorPermission(BasePermission):
    def has_permission(self, request, view):
        return "Supervisor" in request.user["roles"] or "Owner" in request.user["roles"]


class OwnerSupervisorAndEmployeePermission(BasePermission):
    def has_permission(self, request, view):
        return "Supervisor" in request.user["roles"] or "Owner" in request.user[
            "roles"] or "Employee" in request.user["user_types"]


class ProfilePermission(BasePermission):
    def has_permission(self, request, view):
        # TODO: to get user id dynamically
        request_id = request.get_full_path().split("/")[-2]
        return int(request_id) == request.user["user_id"]
