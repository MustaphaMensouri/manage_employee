from .serializers import EmployeeSerializer, TeamSerializer, ContratSerializer, AttendanceSerializer
from .models import Employee, Team, Attendance, Contrat
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from datetime import date,datetime
from collections import defaultdict


# Create your views here.

# all operation about employee
@api_view(['GET', 'POST', 'DELETE'])
def view_employee(request):
    if request.method == "GET":
        # Fetch all employees
        employees = Employee.objects.all()
        
        # Serialize all employee data
        serializer = EmployeeSerializer(employees, many=True)
        serialized_data = serializer.data
        
        # Prepare the final response data with contract expiration status
        response_data = []
        
        for employee_data in serialized_data:
            employee_id = employee_data['id']
            try:
                # Fetch the contract for the employee
                contract = Contrat.objects.get(employee=employee_id)
                # Check if the contract is expired
                is_expired = contract.date_end < date.today()
                
            except Contrat.DoesNotExist:
                is_expired = True  # Assuming no contract means expired
            
            try:
                ferme = Contrat.objects.get(employee=employee_id).ferme.name
            except Contrat.DoesNotExist:
                ferme='noFerme' 
            
            # Add the expiration status to the employee data
            employee_data['contract_expired'] = is_expired
            employee_data['ferme'] = ferme
            response_data.append(employee_data)
        
        return Response(response_data)
    elif request.method == "POST":
        data = request.data
        emp_fields = ['first_name','last_name', 'birthday', 'phone','cin','path_img_cin', 'status_employee', 'team']
        contract_field = ['date_start', 'date_end', 'job_title', 'ferme', 'salary_hour']

        contract_data  = {key: data[key] for key in contract_field if key in data}
        contract_data["status"] = True
        
        emp_data = {key: data[key] for key in emp_fields if key in data}
        serializer_emp = EmployeeSerializer(data=emp_data)

        if serializer_emp.is_valid():
            try:
                with transaction.atomic():
                    employee = serializer_emp.save()
                    
                    contract_data["employee"] = employee.pk
                    serializer_contract = ContratSerializer(data=contract_data)
                    
                    if serializer_contract.is_valid():
                        serializer_contract.save()
                        return Response({'message': 'Successfully created employee and contract.'}, status=status.HTTP_201_CREATED)
                    else:
                        # Rollback the transaction if contract data is invalid
                        raise ValueError(serializer_contract.errors)
                        
            except Exception as e:
                # In case of an exception, it will rollback the transaction
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer_emp.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        data = request.data
        if 'cin' not in data:
            return Response({'error': 'CIN list is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            for cin in data['cin']:
                employee = Employee.objects.get(cin=cin)
                employee.delete()
            return Response({'message': 'Employees deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({'error': 'One or more employees not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def viewTeam(request):
    if request.method == "GET":
        data = Team.objects.all()
        serializer = TeamSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "successfully created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "this is not valide"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
def viewPresence(request):        
    if request.method == "POST":
        data = request.data['data']
        if 'cin' not in data:
            return Response({'error': 'CIN list is required.'}, status=status.HTTP_400_BAD_REQUEST)
        list_presence = []

        for i in data['cin']:
            date_field = data['date'] if 'date' in data else str(date.today())
            list_presence.append({'employee':i, 'status': True, 'date':date_field})
        serializer = AttendanceSerializer(data=list_presence, many=True)
        
        if serializer.is_valid():
            count = 0
            for i in list_presence:
                ser = AttendanceSerializer(data=i)
                if Attendance.employee_attendance_exists(i['employee'], i['date']):
                    pass
                else:
                    ser.is_valid()
                    ser.save()
                    count += 1

            return Response({'message': f"{count}"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "this is not valide"}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"error": "Date parameter is missing"}, status=400)
        
        try:
            date_ = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return Response({"error": "Date format should be YYYY-MM-DD"}, status=400)
        
        result = Attendance.objects.filter(date__month=date_.month, date__year=date_.year)
        serializer = AttendanceSerializer(result, many=True)
        data = serializer.data
        print("data###################",data)

        salary_heur = []
        # Grouping data by employee
        grouped_data = defaultdict(list)
        for entry in data:
            grouped_data[entry['employee']].append(entry['date'])
            salary_heur.append(Contrat.objects.get(employee=Employee.objects.get(cin=entry['employee']).id).salary_hour)

        
        
        

        # Formatting the grouped data
        formatted_data = [{'name': Employee.objects.get(cin=employee).first_name+ " " + Employee.objects.get(cin=employee).last_name, 'cin': employee,'dates': dates, 'salary': (salary_heur[index]*8)*len(dates)} for index, (employee, dates) in enumerate(grouped_data.items())]

        return Response(formatted_data)

