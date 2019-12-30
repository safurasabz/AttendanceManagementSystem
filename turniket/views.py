from django.shortcuts import render
import openpyxl, re
from turniket.models import Excel, Staff, Log, Permissions
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, F, Value

# Create your views here.

app_name = "turniket"

def addperm(request):
    data = request.POST.copy()
    ddd = str(data["date"])
    perm = Permissions(name=data["staffname"], date=data["date"], hour1=data["hour1"]+":00", hour2=data["hour2"]+":00",
                       reason=data["reason"], note =data["note"])
    perm.save()
    print("saved")
    return render(request, 'turniket/index.html', {"data": data})


def index(request):
    i1 = 0
    staff = Staff.objects.all()
    if "GET" == request.method:
        return render(request, 'turniket/index.html', {"names": Staff.objects.all()})
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
                    print(actions[0])
                    del actions[0]
                    if logcame[:2] != "" and int(logcame[:2]) < 9 and logcame!=noway:
                        logearly_came = convertTimeToStr(difference('09:00:00', logcame))
                        loglate_came = "0"
                    elif logcame[:2] != "" and int(logcame[:2]) >= 9 and logcame!=noway:
                        logearly_came = "0"
                        loglate_came = convertTimeToStr(difference(logcame, '09:00:00'))
                else:
                    logcame = noway
                    loglate_came = noway
                    logearly_came = noway
                    logoveralldec = 0
                    logoverallgdec = 0
                    logoverall = noway
                    logoverallg = noway


                if len(hours) > 0 and actions[len(hours)-1] == "выход" and hours[-1] != "":
                    loggone = hours[len(hours)-1]
                    hours.remove(loggone)
                    del actions[len(actions)-1]
                    if loggone[:2] != "" and int(loggone[:2]) >= 18 and loggone!=noway:
                        loglate_gone = convertTimeToStr(difference(loggone, '18:00:00'))
                        logearly_gone = "0"
                    elif loggone[:2] != "" and int(loggone[:2]) < 18 and loggone!=noway:
                        logearly_gone = convertTimeToStr(difference('18:00:00', loggone))
                        loglate_gone = "0"
                else:
                    loggone = noway
                    logearly_gone = noway
                    loglate_gone = noway
                    logoverall = noway
                    logoveralldec = 0
                    logoverallgdec = 0
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
                        if int(hours[j][:2])<13:
                            left = hours[j]
                        elif int(hours[j][:2])>=14:
                            left = hours[j]
                        else:
                            left = '14:00:00'

                        if int(hours[j+1][:2])< 13:
                            entr = hours[j+1]
                        elif int(hours[j+1][:2])>=14:
                            entr = hours[j+1]
                        else:
                            entr = '13:00:00'
                        print("entrleftbefor", entr, left)
                        if int(entr[:2])>int(left[:2]):
                            print("entrleft", entr, left)
                            distractiondec = distractiondec + difference(entr, left)


                if loggone != noway and logcame != noway:
                    if int(loggone[:2]) >=18:
                        last =  "18:00:00"
                    else:
                        last = loggone
                    if int(logcame[:2]) < 9:
                        first = "09:00:00"
                    else:
                        first = logcame
                    if int(loggone[:2])<=13:
                        gonebefbr =  0
                    else:
                        gonebefbr = difference('14:00:00', '13:00:00')
                    logoverall = convertTimeToStr(
                        difference(loggone, logcame) - distractiondec - gonebefbr)
                    logoverallg = convertTimeToStr(
                        difference(last, first) - distractiondec - gonebefbr)

                if len(Permissions.objects.filter(name=data['name'], date=logdate))>0:
                    permission = Permissions.objects.filter(name=data['name'], date=logdate)
                    for perm in permission:
                        print(perm.hour1, type(perm.hour1))
                        if int(perm.hour1[:2]) <= 13 <= int(perm.hour2[:2]):
                            nondist = difference(perm.hour2, perm.hour1) - difference('14:00:00', '13:00:00')
                            distractiondec = distractiondec - nondist
                            logbuild_exit = logbuild_exit - 1
                logoveralldec = convertStrToSec(logoverall)
                logoverallgdec = convertStrToSec(logoverallg)
                distractionstr = convertTimeToStr(distractiondec)
                if convertStrToSec(loglate_came)>0:
                    loglate_camebin = 1
                else:
                    loglate_camebin=0
                print(logdate, logfullname, logcame, loggone,
                      logearly_came, loglate_came, logearly_gone, loglate_gone, logbuild_exit,distractionstr,
                      distractiondec, logoverall, logoverallg)

                #whether the employee has permission for current date
                p = Permissions.objects.filter(name=data['name'], date=date)
                if  len(p)>0:
                    for perm in p:
                        logpermission = str(perm.hour1)[:5] + "-" + str(perm.hour2)[:5]
                        logpermissionreason = perm.reason + " not:" + perm.note
                else:
                    logpermission = "-"
                    logpermissionreason = "-"

                logdata = Log(
                    date=logdate,
                    fullname=logfullname,
                    came=logcame,
                    gone=loggone,
                    early_came=logearly_came,
                    late_came=loglate_came,
                    late_camebin = loglate_camebin,
                    early_gone=logearly_gone,
                    late_gone=loglate_gone,
                    build_exit=logbuild_exit,
                    distraction=distractionstr,
                    overall_hourdec = logoveralldec,
                    overall_ghourdec = logoverallgdec,
                    overall_ghour=logoverallg,
                    overall_hour=logoverall,
                    permission=logpermission,
                    permissionreason=logpermissionreason)

                logdata.save()

        return render(request, 'turniket/index.html', {"excel_data": Log.objects.all(), "names": staff})





def filter(request):
    data = request.POST.copy()
    ddd = str(data["date"])
    keys = data.keys()
    for temp in Log.objects.filter(fullname=data['fullname'], date=str(data["date"])):
        if temp.overall_ghour!="0" and temp.overall_hour!="0":
            graphichour = convertStrToSec(temp.overall_ghour)
            totalhour = convertStrToSec(temp.overall_hour)
        else:
            graphichour = convertStrToSec("0 s 0 deq 0 san")
            totalhour = convertStrToSec("0 s 0 deq 0 san")
        late = convertStrToSec(temp.late_came)

    if data['fullname']!= '':
        if data['date']!='':
            if 'overtime' in keys:
                if 'belate' in keys:
                    excel_file = Log.objects.filter(fullname=data['fullname'], date=str(data["date"]),
                                                    overall_hourdec__gt=F("overall_ghourdec"), late_camebin__gt=0 )
                else:
                    excel_file = Log.objects.filter(fullname=data['fullname'], date=str(data["date"]),
                                                    overall_hourdec__gt=F("overall_ghourdec"))
            else:
                if 'belate' in keys:
                    excel_file = Log.objects.filter(fullname=data['fullname'], date=str(data["date"]), late_camebin__gt=0 )
                else:
                    excel_file = Log.objects.filter(fullname=data['fullname'], date=str(data["date"]))
        else:
            if 'overtime' in keys:
                if 'belate' in keys:
                    excel_file = Log.objects.filter(fullname=data['fullname'], overall_hourdec__gt=F("overall_ghourdec"), late_camebin__gt=0 )
                else:
                    excel_file = Log.objects.filter(fullname=data['fullname'], overall_hourdec__gt=F("overall_ghourdec") )
            else:
                if 'belate' in keys:
                    excel_file = Log.objects.filter(fullname=data['fullname'], late_camebin__gt=0 )
                else:
                    excel_file = Log.objects.filter(fullname=data['fullname'] )
    else:
        if data['date'] != '':
            if 'overtime' in keys:
                if 'belate' in keys:
                    excel_file = Log.objects.filter(date=data['date'], overall_hourdec__gt=F("overall_ghourdec"), late_camebin__gt=0 )
                else:
                    excel_file = Log.objects.filter(date=data['date'], overall_hourdec__gt=F("overall_ghourdec") )
            else:
                if 'belate' in keys:
                    excel_file = Log.objects.filter(date=data['date'], late_camebin__gt=0 )
                else:
                    excel_file = Log.objects.filter(date=data['date'])
        else:
            if 'overtime' in keys:
                if 'belate' in keys:
                    excel_file = Log.objects.filter(overall_hourdec__gt=F("overall_ghourdec"), late_camebin__gt=0 )
                else:
                    excel_file = Log.objects.filter(overall_hourdec__gt=F("overall_ghourdec") )
            else:
                if 'belate' in keys:
                    excel_file = Log.objects.filter(late_camebin__gt=0)
                else:
                    excel_file = Log.objects.all()
    return render(request, 'turniket/index.html', {"excel_data": excel_file, "names": Staff.objects.all()})


# def filter(request):
#     if request.method == "GET":
#         return render(request, 'turniket/index.html')
#     return render(request, 'turniket/index2.html')

def addshortday(request):
    if request.method == "GET":
        return render(request, 'turniket/index.html')
    return render(request, 'turniket/index2.html')

def exportreport(request):
    if request.method == "GET":
        return render(request, 'turniket/index.html')
    return render(request, 'turniket/index2.html')

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
        res = str(h) + " s "
        m = (time - (time//3600)*3600)//60
        res = res + str(m) + " dəq "
        s = time - h*3600 - m*60
        res = res + str(s) + " san "
        return res
    else:
        return "0"

def convertStrToSec(timeline):
    print(timeline)
    templist = timeline.split()
    if len(templist)>=5:
        print(templist)
        h = int(templist[0])
        m = int(templist[2])
        s = int(templist[4])
        decimaltime = h*3600 + m*60 + s
        return decimaltime
    else:
        return 0



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