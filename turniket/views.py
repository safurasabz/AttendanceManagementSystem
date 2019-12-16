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
        Log.objects.all().delete()
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
                #logdata.staff_id = Staff.objects.filter().first()
                logdata.date = date
                hours = []
                actions = []

                for i in Excel.objects.filter(name=data['name'], dat=date):
                    hours.append(i.time)
                    actions.append(i.action)
                # print(data['name'], date, hours)
                # print(data['name'], date, actions)
                for j in Excel.objects.filter(name=data['name'], dat=date):
                    c = ""
                    g = ""
                    logdata.fullname = data['name']
                    if len(hours) != 0 and j.action == "вход":
                        logdata.came = hours[0]
                        c = hours[0]
                        if logdata.came[:2] != "" and int(logdata.came[:2]) < 9:
                            logdata.early_came = convertTimeToStr(difference('09:00:00', logdata.came))
                            logdata.late_came = 0
                        elif logdata.came[:2] != "" and int(logdata.came[:2]) >= 9:
                            logdata.early_came = 0
                            logdata.late_came = convertTimeToStr(difference(logdata.came, '09:00:00'))
                        hours.remove(logdata.came)
                        actions.remove(actions[0])

                    if len(hours) >= 2 and j.action == "выход":
                        logdata.gone = hours[len(hours)-1]
                        g = hours[len(hours)-1]
                        if logdata.came[6:] != "" and int(logdata.came[6:]) >= 18:
                            logdata.late_gone = convertTimeToStr(difference(logdata.gone, '18:00:00'))
                            logdata.early_gone = "0"
                        elif logdata.came[6:] != "" and int(logdata.came[6:]) < 18:
                            logdata.early_gone = convertTimeToStr(difference('18:00:00', logdata.gone))
                            logdata.late_gone = "0"
                        hours.remove(logdata.gone)
                        actions.remove(actions[-1])
                    else:
                         logdata.gone = ""
                    count = Excel.objects.filter(name=data['name'], dat=date, action = "выход")
                    logdata.build_exit = len(count)
                    actbin = []
                    distractiondec = 0
                    distractionstr = ""
                    for v in actions:
                        if v == "выход":
                            actbin.append(1)
                        else:
                            actbin.append(0)
                    for j in range(len(hours)-1):
                        if actbin[j] == 1 and actbin[j+1] == 0:
                            distractiondec = distractiondec + difference(hours[j+1], hours[j])
                    distractionstr = convertTimeToStr(distractiondec)
                    logdata.distraction = distractionstr
                    if g != "" and c != "":
                        logdata.overall_hour = convertTimeToStr(difference(g, c) - distractiondec - difference('14:00:00', '13:00:00'))
                        logdata.overall_ghour = convertTimeToStr(difference('18:00:00', '09:00:00') - distractiondec - difference('14:00:00', '13:00:00'))
                    else:
                        logdata.overall_ghour = ""
                        logdata.overall_hour = ""
                    logdata.save()
                # print(data['name'], 'has came', logdata.came)
                # print(data['name'], 'has gone', logdata.gone)
                # print("duration of work", difference(logdata.gone, logdata.came), convertTimeToStr(difference(logdata.gone, logdata.came)))

           # print(data.name, dateslist)

        return render(request, 'turniket/index.html', {"excel_data": Log.objects.all()})


def difference(hour1, hour2):
    if hour1 != "" and hour2 != "":
        h1 = hour1[:2]
        h2 = int(hour2[:2])
        m1 = hour1[3:5]
        m2 = int(hour2[3:5])
        s1 = int(hour1[6:])
        s2 = int(hour2[6:])
        time1 = int(h1)*3600 + int(m1)*60 + s1
        time2 = h2*3600 + m2*60 + s2
        return time1 - time2
    else:
        return 0


def convertTimeToStr(time):
    if time != 0:
        h = time//3600
        res = str(h) + "s "
        m = (time - (time//3600)*3600)//60
        res = res + str(m) + " dəq "
        s = time - h*3600 - m*60
        res = res + str(s) + " san "
        return res
    else:
        return "0"



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