from django.db import models
from general.models import Ferme 

class Team(models.Model):
    name = models.CharField(max_length=256)
    ferme = models.ForeignKey(Ferme, on_delete=models.CASCADE)

class Employee(models.Model):
    # db columns [first_name="test",last_name="test", birthday="test", cin="test", path_img_cin="test", status_employee="test", team]
    first_name = models.CharField(max_length=56)
    last_name = models.CharField(max_length=56)
    birthday = models.DateField(max_length=56)
    cin = models.CharField(max_length=56, unique=True)
    path_img_cin = models.CharField(max_length=512)
    phone = models.CharField(max_length=15, null=True, blank=True)
    status_employee = models.BooleanField(default=True) # is it active or not
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class Contrat(models.Model):
    # ["date_start", "date_end", "job_title", "ferme", "employee", "salary_hour", 'status']
    date_start = models.DateField()
    date_end = models.DateField()
    job_title = models.CharField(max_length=256)
    ferme = models.ForeignKey(Ferme, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary_hour = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    status = models.BooleanField(default=True)
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    status = models.BooleanField(null=False)
    def employee_attendance_exists(cin, date):
        employee = Employee.objects.get(cin=cin)
        return Attendance.objects.filter(employee=employee, date=date).exists()






