from rest_framework import permissions
import api
import pdb

class IsSameHospital(permissions.BasePermission):
    """
    Custom permission to allow doctors of a hospital to only view
    visits of that hospital
    """

    def has_object_permission(self, request, view, obj):
        # Super user can always access
        if request.user.is_superuser:
            return True
        elif type(obj) == api.models.Hospital:
            return request.user.groups.first() == obj.group
        elif type(obj) == api.models.Patient:
            return request.user.groups.first() == obj.hospital.group
        elif type(obj) == api.models.Visit:
            return request.user.groups.first() == obj.patient.hospital.group
        return False
