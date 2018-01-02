from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return JsonResponse({
    'api/': 'Access DataReach API.',
    'admin/': 'Access DataReach API admin panel.',
    'auth/': 'Authenticatication for DataReach API.',
    }, status=200)
