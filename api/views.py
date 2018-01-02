from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from api.models import Hospital, Patient, Visit
from api.serializers import HospitalSerializer, PatientSerializer, VisitSerializer, DoctorSerializer
from api.permissions import IsSameHospital
import pdb

class HospitalViewSet(viewsets.ModelViewSet):
	"""
	RESTful API endpoint for Hospital
	"""
	queryset = Hospital.objects.all()
	serializer_class = HospitalSerializer
	permission_classes = (permissions.IsAuthenticated, IsSameHospital)

	def create(self, request):
		if 'name' not in request.data:
			return JsonResponse({'detail':'Name parameter missing'}, status=422)
		new_group, created = Group.objects.get_or_create(name=request.data['name'])
		if not created:
			return JsonResponse({'detail':'Hospital already exists'}, status=409)
		try:
			new_hospital = Hospital.objects.create(group=new_group)
		except:
			new_group.delete()
			return JsonResponse({'detail':"Could not create new hospital"}, status=500)
		serializer = HospitalSerializer(new_hospital)
		return JsonResponse(serializer.data, status=201)

	def update(self, request, id=None):
		pass

	def destroy(self, request, id=None):
		pass

class DoctorViewSet(viewsets.ModelViewSet):
	"""
	RESTful API endpoint for Doctors
	"""
	queryset = User.objects.all().filter(is_superuser=False)
	serializer_class = DoctorSerializer

	def list(self, request):
		if request.user.is_anonymous():
			return JsonResponse({'detail':'You do not have permission to perform this action.'}, status=403)
		elif request.user.is_superuser:
			all_doctors = User.objects.all().filter(is_superuser=False)
			serializer = DoctorSerializer(all_doctors, many=True)
			return JsonResponse(serializer.data, status=200, safe=False)
		else:
			serializer = DoctorSerializer(request.user)
			return JsonResponse(serializer.data, status=200)

	def create(self, request):
		# validate all required params exist
		if 'username' not in request.data:
			return JsonResponse({'detail':'username parameter missing.'}, status=422)
		if 'email' not in request.data:
			return JsonResponse({'detail':'email parameter missing.'}, status=422)
		if 'first_name' not in request.data:
			return JsonResponse({'detail':'first_name parameter missing.'}, status=422)
		if 'last_name' not in request.data:
			return JsonResponse({'detail':'last_name parameter missing.'}, status=422)
		if 'password' not in request.data:
			return JsonResponse({'detail':'password parameter missing.'}, status=422)
		if 'hospital_group_id' not in request.data:
			return JsonResponse({'detail':'hospital_group_id parameter missing.'}, status=422)
		# validate hospital exists
		try:
			hospital_group = Group.objects.get(id=request.data['hospital_group_id'])
		except Group.DoesNotExist:
			return JsonResponse({'detail':'hospital_group_id does not exist.'}, status=404)
		# validate user with username does not exist
		if User.objects.filter(username=request.data['username']).count() > 0:
			return JsonResponse({'detail':'user with username already exists.'}, status=409)
		# create doctor
		new_doctor = User.objects.create_user(
			username=request.data['username'],
			email=request.data['email'],
			first_name=request.data['first_name'],
			last_name=request.data['last_name'],
			password=request.data['password'],
		)
		# add doctor to correct hospital group
		hospital_group.user_set.add(new_doctor)
		serializer = DoctorSerializer(new_doctor)
		return JsonResponse(serializer.data, status=201)

class PatientViewSet(viewsets.ModelViewSet):
	"""
	RESTful API endpoint for Patients
	"""
	queryset = Patient.objects.all()
	serializer_class = PatientSerializer
	permission_classes = (permissions.IsAuthenticated, IsSameHospital)

class VisitViewSet(viewsets.ModelViewSet):
	"""
	RESTful API endpoint for Visits
	"""
	queryset = Visit.objects.all()
	serializer_class = VisitSerializer
	permission_classes = (permissions.IsAuthenticated, IsSameHospital)

	def list(self, request):
		if request.user.is_superuser:
			all_visits = Visit.objects.all()
			serializer = VisitSerializer(all_visits, many=True)
			return JsonResponse(serializer.data, status=200, safe=False)
		else:
			subset_visits = Visit.objects.all().filter(patient__hospital__group__id=request.user.groups.first().id)
			serializer = VisitSerializer(subset_visits, many=True)
			return JsonResponse(serializer.data, status=200, safe=False)
