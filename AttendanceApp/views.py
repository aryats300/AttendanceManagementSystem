# from django.shortcuts import render, redirect
# from django.http import HttpResponse, JsonResponse
# from .forms import CSVUploadForm
# from django.views.decorators.csrf import csrf_exempt
# from datetime import datetime


# import datetime
# from django.core.serializers.json import DjangoJSONEncoder
# from .models import PunchAttendance,Attendance
# import csv
# import io
# import json
# # Create your views here.

# @csrf_exempt
# def upload_csv(request):
#     if request.method == 'POST':
#         form = CSVUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Read the uploaded CSV file
#             csv_file = request.FILES['csv_file']
#             data_set = csv_file.read().decode('UTF-8')
#             io_string = io.StringIO(data_set)
#             headers = []
#             data = []
#             # Loop through each row in the CSV file
#             for row in csv.reader(io_string, delimiter=',', quotechar='"'):
#                 if not headers:
#                     # The first row contains column headers, so we save them in the 'headers' list
#                     headers = row
#                 else:
#                     # The rest of the rows contain data, so we create a dictionary with the column headers as keys and row values as values
#                     item = {}
#                     for i, header in enumerate(headers):
#                         item[header] = row[i]
#                     data.append(item)
#                     print(data)
#                     # Create a new PunchAttendance object for the current row of data
#                     employee_id = item["Employee ID"]
#                     if item['Check-in']:
#                         check_in = datetime.datetime.strptime(item['Check-in'], '%m/%d/%Y %I:%M %p')
#                     # else:
#                     #     check_out = None

#                     if item['Check-out']:
#                         check_out = datetime.datetime.strptime(item['Check-out'], '%m/%d/%Y %I:%M %p')
#                     # else:
#                     #     check_out = None
#                     existing_attendance = PunchAttendance.objects.filter(check_in=check_in).first()
#                     if not existing_attendance:
#                     # if check_in not in PunchAttendance:
#                         attendance = PunchAttendance(
#                             employee_id=employee_id,
#                             check_in=check_in,
#                             check_out=check_out
#                         )
#                         attendance.save()
            
#             json_data = json.dumps(data, indent=2)
            
#             # Set the JSON data in the session
#             request.session['json_data'] = json_data
            
#             return redirect('success')
#     else:
#         form = CSVUploadForm()
#     return render(request, 'upload_csv.html', {'form': form})


# def success(request):
    
#     json_data = request.session.get('json_data')
  
#     if json_data:
#         data = json.loads(json_data)
        
       
#         for row in data:
#             employee_id = row["Employee ID"]
#             status = '0'  # Initialize status as '0' by default
            
#             if "Check-in" in row and row["Check-in"]:
#                 check_in = datetime.datetime.strptime(row["Check-in"], '%m/%d/%Y %I:%M %p')
#                 month = check_in.strftime("%B")
#                 day = check_in.day
#                 year = check_in.year
#                 checkin_time = check_in
#             else:
#                 status = '0'
                
#             if "Check-out" in row and row["Check-out"]:
#                 check_out = datetime.datetime.strptime(row["Check-out"], '%m/%d/%Y %I:%M %p')
#                 checkout_time = check_out
#             else:
#                 status = '0'
                
#             if "Check-in" in row and "Check-out" in row and row["Check-in"] and row["Check-out"]:
#                 time_difference = check_out - check_in
#                 hours_difference = time_difference.total_seconds() / 3600.0
#                 if hours_difference >= 8:
#                     status = '1'
#                 else:
#                     status = '0'
#             else:
#                 hours_difference = 0
            
#             existing_attendance = Attendance.objects.filter(employee_id=employee_id, year=year, month=month, day=day).first()
#             if not existing_attendance:
#                 attendance = Attendance(
#                     employee_id=employee_id,
#                     year=year,
#                     month=month,
#                     day=day,
#                     attendance=status,
#                     # work_hours=hours_difference
#                 )
#                 attendance.save()
#                 print("attendance:", attendance)


#     data = list(Attendance.objects.all().values())
#     json_data = json.dumps(data)
   

#     return HttpResponse(json_data)
        


from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import CSVUploadForm
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import datetime
from django.core.serializers.json import DjangoJSONEncoder
from .models import PunchAttendance, Attendance
import csv
import io
import json
from collections import defaultdict

# Create your views here.

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the uploaded CSV file
            csv_file = request.FILES['csv_file']
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            headers = []
            data = []
            # Loop through each row in the CSV file
            for row in csv.reader(io_string, delimiter=',', quotechar='"'):
                if not headers:
                    # The first row contains column headers, so we save them in the 'headers' list
                    headers = row
                else:
                    # The rest of the rows contain data, so we create a dictionary with the column headers as keys and row values as values
                    item = {}
                    for i, header in enumerate(headers):
                        item[header] = row[i]
                    data.append(item)
                    print(data)
                    # Create a new PunchAttendance object for the current row of data
                    employee_id = item["Employee ID"]
                    if item['Check-in']:
                        check_in = datetime.datetime.strptime(item['Check-in'], '%m/%d/%Y %I:%M %p')
                    # else:
                    #     check_out = None

                    if item['Check-out']:
                        check_out = datetime.datetime.strptime(item['Check-out'], '%m/%d/%Y %I:%M %p')
                    # else:
                    #     check_out = None
                    existing_attendance = PunchAttendance.objects.filter(check_in=check_in).first()
                    if not existing_attendance:
                    # if check_in not in PunchAttendance:
                        attendance = PunchAttendance(
                            employee_id=employee_id,
                            check_in=check_in,
                            check_out=check_out
                        )
                        attendance.save()
            
            json_data = json.dumps(data, indent=2)
            
            # Set the JSON data in the session
            request.session['json_data'] = json_data
            
            return redirect('success')
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})


def success(request):
    
    json_data = request.session.get('json_data')
  
    if json_data:
        data = json.loads(json_data)
        
        employee_data = defaultdict(list)

        for row in data:
            employee_id = row["Employee ID"]
            
            if "Check-in" in row and row["Check-in"]:
                check_in = datetime.datetime.strptime(row["Check-in"], '%m/%d/%Y %I:%M %p')
                checkin_time = check_in
            else:
                checkin_time = None
                
            if "Check-out" in row and row["Check-out"]:
                check_out = datetime.datetime.strptime(row["Check-out"], '%m/%d/%Y %I:%M %p')
                checkout_time = check_out
            else:
                checkout_time = None
            
            if checkin_time and checkout_time:
                employee_data[(employee_id, check_in.date())].append((checkin_time, checkout_time))

        for (employee_id, date), check_times in employee_data.items():
            check_times.sort()  # Sort the check-in and check-out times in ascending order
            
            first_checkin, last_checkout = check_times[0][0], check_times[-1][1]
            
            time_difference = last_checkout - first_checkin
            hours_difference = time_difference.total_seconds() / 3600.0
            
            status = '1' if hours_difference >= 8 else '0'
            
            month = first_checkin.strftime("%B")
            day = first_checkin.day
            year = first_checkin.year
            
            existing_attendance = Attendance.objects.filter(employee_id=employee_id, year=year, month=month, day=day).first()
            if not existing_attendance:
                attendance = Attendance(
                    employee_id=employee_id,
                    year=year,
                    month=month,
                    day=day,
                    attendance=status,
                    # work_hours=hours_difference
                )
                attendance.save()
                print("attendance:", attendance)


    data = list(Attendance.objects.all().values())
    json_data = json.dumps(data)
   

    return HttpResponse(json_data)


