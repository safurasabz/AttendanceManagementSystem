from django.shortcuts import render
import openpyxl, re
from turniket.models import Excel, Staff, Log
from django.utils import timezone

# Create your views here.


def index(request):
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
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
        noway = "NODATA"
        # getting a particular sheet
        worksheet = wb["Sheet1"]
        excel_data = list()
        Excel.objects.all().delete()
        Log.objects.all().delete()
        #excelfileden oxuyub liste yazmaq ve listi dba save etmek
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            if row_data[9] == "" or row_data[0] == "" or row_data[9] is None or row_data[0] is None or row_data[9] == "None" or row_data[0]=="None" :
                continue
            else:
                dataRow = Excel(dat=row_data[0], time=row_data[1], action=row_data[3], name=row_data[9])
                dataRow.save()
                excel_data.append(row_data)
        dateslist = []
        #faylda distinct insalari iterate edir
        for data in Excel.objects.values('name').distinct():
            i1 = i1 + 1
            print("Reading ",i1,"st person who is ", data['name'], type(data['name']))
            #fayldaki adlarin her birini ayriliqda sechib obyektleri dates-e yigir.
            dates = Excel.objects.filter(name=data['name'])
            #obyektleri yigdiqdan sonra iterate edib list yaradir
            for date in dates:
                dateslist.append(date.dat)
            #distinctlesdhrir dateslist date stringini saxlayir
            dateslist = list(dict.fromkeys(dateslist))
            #her bir date-e gore log db uchun record yigilmaya bashlayir
            #her bir insana aid olan date-leri bir br iterate edirik
            for date in dateslist:
                logdate = date
                hours = []
                actions = []
                logfullname = data['name']
                #her bir insanin bir gun ichinde aid olan saatlari ve actionlari list e yigir ardicil
                for i in Excel.objects.filter(name=data['name'], dat=date):
                    hours.append(i.time)
                    actions.append(i.action)
                print(hours)
                print(actions)
                logbuild_exit = 0
                #gelme tarixi varsa gecikmeni tez gelmeni ve gelme vaxtini tapir
                if len(hours) > 0 and actions[0] == "вход" and hours[0] != "":
                    logcame = hours[0]
                    hours.remove(logcame)
                    actions.remove(actions[0])
                    if logcame[:2] != "" and int(logcame[:2]) < 9:
                        logearly_came = convertTimeToStr(difference('09:00:00', logcame))
                        loglate_came = 0
                    elif logcame[:2] != "" and int(logcame[:2]) >= 9:
                        logearly_came = 0
                        loglate_came = convertTimeToStr(difference(logcame, '09:00:00'))
                else:
                    logcame = noway
                    loglate_came = noway
                    logearly_came = noway
                    logoverall = noway
                    logoverallg = noway


                if len(hours) > 0 and actions[len(hours)-1] == "выход" and hours[-1] != "":
                    loggone = hours[len(hours)-1]
                    hours.remove(loggone)
                    actions.remove(actions[-1])
                    if loggone[6:] != "" and int(loggone[:2]) >= 18:
                        loglate_gone = convertTimeToStr(difference(loggone, '18:00:00'))
                        logearly_gone = "0"
                    elif logcame[6:] != "" and int(logcame[:2]) < 18:
                        logearly_gone = convertTimeToStr(difference('18:00:00', loggone))
                        loglate_gone = "0"
                else:
                    loggone = noway
                    logearly_gone = noway
                    loglate_gone = noway
                    logoverall = noway
                    logoverallg = noway
                print(logfullname)
                print(hours)
                print(actions)
                actbin = []
                for v in actions:
                    if v == "выход":
                        actbin.append(1)
                    else:
                        actbin.append(0)
                logbuild_exit = sum(actbin)

                distractiondec = 0
                distractionstr = ""
                for j in range(len(hours) - 1):
                    if actbin[j] == 1 and actbin[j + 1] == 0:
                        distractiondec = distractiondec + difference(hours[j + 1], hours[j])
                distractionstr = convertTimeToStr(distractiondec)

                if loggone != noway and logcame != noway:
                    logoverall = convertTimeToStr(
                        difference(loggone, logcame) - distractiondec - difference('14:00:00', '13:00:00'))
                    logoverallg = convertTimeToStr(
                        difference('18:00:00', '09:00:00') - distractiondec - difference('14:00:00', '13:00:00'))
                print(logdate, logfullname, logcame, loggone,
                      logearly_came, loglate_came, logearly_gone, loglate_gone, logbuild_exit,distractionstr,
                      distractiondec, logoverall, logoverallg)

                logdata = Log(
                    date=logdate,
                    fullname=logfullname,
                    came=logcame,
                    gone=loggone,
                    early_came=logearly_came,
                    late_came=loglate_came,
                    early_gone=logearly_gone,
                    late_gone=loglate_gone,
                    build_exit=logbuild_exit,
                    distraction=distractionstr,
                    overall_ghour=logoverallg,
                    overall_hour=logoverall)
                logdata.save()

        return render(request, 'turniket/index.html', {"excel_data": Log.objects.all()})


def difference(hour1, hour2):
    if hour1 != " " and hour2 != " ":
        print(hour1, hour2)
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