from rest_framework import serializers
from .models import Employee, Team, Contrat, Attendance
from general.models import Ferme

class EmployeeSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(slug_field='name', queryset=Team.objects.all())
    class Meta:
        model = Employee
        fields = ['id', 'first_name','last_name', 'birthday', 'cin', 'phone','path_img_cin', 'status_employee', 'team']


class ContratSerializer(serializers.ModelSerializer):
    ferme = serializers.SlugRelatedField(slug_field='name', queryset=Ferme.objects.all())
    employee = serializers.SlugRelatedField(slug_field='id', queryset=Employee.objects.all())
    class Meta:
        model = Contrat
        fields = ['id','date_start', 'date_end', 'job_title', 'ferme', 'employee', 'salary_hour', 'status']


class TeamSerializer(serializers.ModelSerializer):
    ferme = serializers.SlugRelatedField(slug_field='name', queryset=Ferme.objects.all())
    class Meta:
        model = Team
        fields = ['id','name', 'ferme']

class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.SlugRelatedField(slug_field='cin', queryset=Employee.objects.all())
    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'date', 'status']



