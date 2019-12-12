from django.shortcuts import render
import openpyxl, re
from turniket.models import Excel, Staff, Log
from django.utils import timezone

# Create your views here.


def index(request):
    if "GET" == request.method:
        return render(request, 'turniket/index.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)
        # f = open("logfile.txt", "a")
        # print ("")

        # getting all sheets
        sheets = wb.sheetnames
        # print("sheets", type(sheets),sheets)
        # f.write(sheets)

        # getting a particular sheet
        worksheet = wb["Sheet1"]
        excel_data = list()
        Excel.objects.all().delete()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            dataRow = Excel(dat=row_data[0], time=row_data[1], action=row_data[3], name=row_data[9])
            dataRow.save()

            excel_data.append(row_data)
        print("done!")
        dateslist = []

        for data in Excel.objects.values('name').distinct():
            dates = Excel.objects.filter(name=data['name'])
            for date in dates:
                dateslist.append(date.dat)
            dateslist = list(dict.fromkeys(dateslist))
            for date in dateslist:
                logdata = Log()
                logdata.staff_id = Staff.objects.filter().first()
                logdata.date = date
                hours = []
                actions = []
                for i in Excel.objects.filter(name=data['name'], dat=date):
                    hours.append(i.time)
                    actions.append(i.action)
                print(data['name'], date, hours)
                print(data['name'], date, actions)
                for j in Excel.objects.filter(name=data['name'], dat=date):
                    if len(hours) != 0 and j.action == "вход":
                        logdata.came = hours[0]
                        c=hours[0]
                        #if int(logdata.came[:2])<9:
                           # logdata.early_came =
                    if len(hours) >= 2 and j.action == "выход":
                        logdata.gone = hours[len(hours)-1]
                        g=hours[len(hours)-1]
                    else:
                        logdata.gone = "don't exist"

                print(data['name'], 'has came', logdata.came)
                print(data['name'], 'has gone', logdata.gone)
                print("duration of work", difference(logdata.gone, logdata.came), convertTimeToStr(difference(g, c)))

           # print(data.name, dateslist)

        return render(request, 'turniket/index.html', {"excel_data": Excel.objects.all()})


def difference(hour1, hour2):
    h1 = int(hour1[:2])
    h2 = int(hour2[:2])
    m1 = int(hour1[3:5])
    m2 = int(hour2[3:5])
    s1 = int(hour1[6:])
    s2 = int(hour2[6:])
    time1 = h1*3600 + m1*60 + s1
    time2 = h2*3600 + m2*60 + s2
    return time1 - time2


def convertTimeToStr(time):
    h = time//3600
    res = str(h) + "hour"
    m = (time - (time//3600)*3600)//60
    res = res + str(m) + "minutes"
    s = time - h*3600 - m*60
    res = res + str(s) + "seconds"
    return res



       # namelist = []
       # person = Staff()
       # names = Excel.objects.values('name').distinct()
       # print(names)
       # for nam in names:
       #     person = Staff()
       #     print(nam['name'])
       #     person.name = nam['name']
       #     person.excel_name = nam['name']
       #     person.status = 1
       #     person.save()