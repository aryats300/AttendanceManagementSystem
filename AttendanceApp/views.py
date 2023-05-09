from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import CSVUploadForm
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


import datetime
from django.core.serializers.json import DjangoJSONEncoder
from .models import PunchAttendance,Attendance
import csv
import io
import json
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
            # print('json data',json_data)
            # Set the JSON data in the session
            request.session['json_data'] = json_data
            
            return redirect('success')
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})


def success(request):
    
    json_data = request.session.get('json_data')
    print('json_data', json_data)
    if json_data:
        data = json.loads(json_data)
        for row in data:
            employee_id = row["Employee ID"]
            if row["Check-in"]:
                check_in = datetime.datetime.strptime(row["Check-in"], '%m/%d/%Y %I:%M %p')
                month=check_in.strftime("%B")
                day=check_in.day
                year=check_in.year
                checkin_time=check_in
            else:
                status = '0'
            if row["Check-out"]:
                check_out=datetime.datetime.strptime(row["Check-out"],'%m/%d/%Y %I:%M %p')
                checkout_time=check_out
            else:
                status = '0'
            if check_in and check_out:
                time_difference=check_out - check_in
                hours_difference=time_difference.total_seconds() / 3600.0
                if hours_difference >=8:
                    status = '1'
                else:
                    status = '0'
            else:
                hours_difference = 0
                status = '0'
            
            existing_attendance = Attendance.objects.filter(employee_id=employee_id, year=year, month=month, date=day).first()
            if not existing_attendance:
                attendance = Attendance(
                    employee_id=employee_id,
                    year=year,
                    month=month,
                    date=day,
                
                    attendance=status,
                    # work_hours=hours_difference
                )
                attendance.save()
                print("attendance:",attendance)


    data = list(Attendance.objects.all().values())
    json_data = json.dumps(data)

    return HttpResponse(json_data)
        


