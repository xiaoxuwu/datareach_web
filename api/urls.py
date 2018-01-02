from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.DefaultRouter()
router.register(r'hospitals', views.HospitalViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'visits', views.VisitViewSet)
router.register(r'doctors', views.DoctorViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
