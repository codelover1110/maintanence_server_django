from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import User, TechnicalCatergory, MetaData_Main, MetaData_Activity, MetaData_Archive
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
from django.core import serializers

from datetime import datetime
from dateutil.parser import parse
import pandas as pd

from django.core.mail import send_mail

from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
import random
import string
import threading
import time
from django.utils import timezone

# Create your views here.


def getUser(request, email, password):
    try:
        user = get_object_or_404(User, email=email)
        if user.password == password:
            if user.active == 'Active':
                data = {
                    'email': user.email,
                    'password': user.password
                }
            else:
                return JsonResponse({'active': 'Inactive'})

        else:
            data = {
                'email': user.email,
                'password': ''
            }
    except:
        data = {
            'email': '',
            'password': ''
        }
    return JsonResponse(data)


def getAdminUser(request):
    userInfor = json.loads(request.body.decode('utf-8'))
    username = userInfor['username']
    try:
        user = get_object_or_404(User, user_name=username)
        if user.password == userInfor['password']:
            if user.user_authority == 'Admin' and user.active == 'Active':
                data = {
                    'user_name': user.user_name,
                    'password': user.password
                }
            else:
                return JsonResponse({'Authority': 'false'})
        else:
            data = {
                'user_name': user.user_name,
                'password': ''
            }
    except:
        data = {
            'user_name': '',
            'password': ''
        }

    return JsonResponse(data)

def getUserMobile(request, user_name, password):
    try:
        user = get_object_or_404(User, user_name=user_name)
        if user.password == password:
            if user.active == 'Active':
                data = {
                    'user_name': user.user_name,
                    'password': user.password,
                    'autherity': user.user_authority
                }
                print(data)

            else:
                return JsonResponse({'Authority': 'false'})
        else:
            data = {
                'user_name': user.user_name,
                'password': ''
            }
    except:
        data = {
            'user_name': '',
            'password': ''
        }

    return JsonResponse(data)


def getAdminUsers(request):
    users = User.objects.all()
    user_list = []
    for user in users:
        item = model_to_dict(user)
        user_list.append(item)

    return JsonResponse(user_list, safe=False)


def addUser(request):
    try:
        User.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            password=request.POST['password'],
            active="Inactive",
            authority="Mobile"
        )
        data = {"success": "true"}
    except:
        data = {"success": "false"}

    return JsonResponse(data)


def addAdminUser(request):
    if request.method == "POST":
        details = json.loads(request.body.decode('utf-8'))
    try:
        User.objects.create(
            email=details['email'],
            password=details['password'],
            user_name=details['username']
        )
        data = {"success": "true"}
    except:
        data = {"success": "false"}

    return JsonResponse(data)


# CRUD user at Web page
def createUser(request):
    content = json.loads(request.POST.get('content'))
    print(content)
    try:
        test = model_to_dict(User.objects.get(user_name=content['username']))
        if test['user_name'] != '':
            return JsonResponse({"success": "false"})
        email_test = model_to_dict(User.objects.get(email=content['email']))
        if email_test['email'] != '':
            return JsonResponse({"success": "email_false"})
    except:
        print("ok")
    try:
        User.objects.create(
            user_name=content['username'],
            name=content['name'],
            email=content['email'],
            password=content['password'],
            company=content['company'],
            phone=content['phone'],
            user_authority=content['authority'],
            active=content['active'],
            technical_authority=content['technical']
        )
        data = {"success": "true"}
    except:
        data = {"success": "email_false"}
    return JsonResponse(data)


def editUser(request, id):
    user = model_to_dict(User.objects.get(id=id))
    return JsonResponse(user)


def updateUser(request, id):
    content = json.loads(request.POST.get('content'))
    try:
        test = model_to_dict(User.objects.get(user_name=content['username']))
        if test["id"] != int(id):
            return JsonResponse({"success": "false"})
        email_test = model_to_dict(User.objects.get(email=content['email']))
        if email_test['email'] != content['email']:
            return JsonResponse({"success": "email_false"})
    except:
        print("ok")
    try:
        user = User.objects.get(id=id)
        user.name = content['name']
        user.user_name = content['username']
        user.phone = content['phone']
        user.password = content['password']
        user.email = content['email']
        user.user_authority = content['authority']
        user.active = content['active']
        user.company = content['company']
        user.technical_authority = content['technical']
        user.save()
        data = {"success": "true"}
    except:
        print("final_except")
        data = {"success": "email_false"}
    return JsonResponse(data)


def home(request):
    return HttpResponse('Hello, Server!')


def deleteAdminUser(request, id):
    user = User.objects.get(id=id)
    if user:
        user.delete()
        return JsonResponse({'success': 'true'})
    else:
        return JsonResponse({'success': 'false'})


def deleteCustomerUser(request, id):
    user = VoteData.objects.get(id=id)
    if user:
        user.delete()
        return JsonResponse({'success': 'true'})
    else:
        return JsonResponse({'success': 'false'})


# CRUD metamain data
def createMetaMainData(request):
    try:
        metaImage = (request.FILES['cover'])
    except:
        metaImage = {}
    content = json.loads(request.POST.get('content'))
    # try:
    print(content)
    MetaData_Main.objects.create(
        meta_data_picture=metaImage,
        technical_category=content['technical'],
        equipment_name=content['equipmentName'],
        nfc_tag=content['nfcTag'],
        service_interval=content['serviceInterval'],
        legit=content['legal'],
        expected_service=content['expectedService'],
        latest_service=content['latestService'],
        contacts=content['contacts'],
        reminder_month=content['reminderMonth'],
        reminder_week=content['reminderWeek'],
        reminder_flag='0',
        longitude=content['longitude'],
        latitude=content['latitude'],
    )
    data = {"success": "true"}
    # except:
    #   data = {"success": "false"}

    return JsonResponse(data)


def getMetaMaindatas(request):
    metaDatas = MetaData_Main.objects.all()
    data_list = []
    x = threading.Thread(target=thread_func, args=("AnJongHyok",))
    x.start()
    for metaData in metaDatas:
        item = model_to_dict(metaData)
        if (item.get('meta_data_picture')):
            item['meta_data_picture'] = str(item.get('meta_data_picture'))
        data_list.append(item)
    return JsonResponse(data_list, safe=False)


def thread_func(arg1):
    while True:
        metaDatas = MetaData_Main.objects.all()
        for metaData in metaDatas:
            item = model_to_dict(metaData)
            if ((item["reminder_month"] == None) or item["reminder_month"] == ""):
                reminderMonth = 0
            else:
                reminderMonth = int(item["reminder_month"])
            if (item["reminder_week"] == None or item["reminder_week"] == ""):
                reminderWeek = 0
            else:
                reminderWeek = int(item["reminder_week"])

            diff = (((item["expected_service"]).replace(tzinfo=None) - (datetime.now())).total_seconds())/3600
            reminderTime = (reminderMonth * 30 * 24) + (reminderWeek * 7 * 24)
            nowDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if ((diff < reminderTime)):
              if(item["reminder_flag"] != '1'):
                convertJsons = json.loads(item["contacts"])
                for convertJson in convertJsons:
                    contact_email = (convertJson['label'])
                    user_name = (model_to_dict(User.objects.get(email=contact_email)))["user_name"]
                    sendmailReminder(user_name, contact_email, nowDate, item["expected_service"], item["equipment_name"], item["technical_category"])
                main_data = get_object_or_404(MetaData_Main, id=item["id"])
                main_data.reminder_flag = "1"
                main_data.save()
        time.sleep(10)

def sendmailReminder(user_name, user_email, reset_time, expected_date, equipment_name, technical_category):
    print(user_name, user_email, reset_time, expected_date, equipment_name)
    ctx = {
        'user': user_name,
        'reset_time': reset_time,
        'expected_date' : expected_date,
        'equipment_name' : equipment_name,
        'technical_catetory' : technical_category
    }
    message = get_template('reminder.html').render(ctx)
    msg = EmailMessage(
        'Subject',
        message,
        'norepleymaintenance@hotmail.com',
        [user_email],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    return HttpResponse('Mail successfully sent')

def getMetaMainData(request, id):
    metadata = model_to_dict(MetaData_Main.objects.get(id=id))
    metadata['meta_data_picture'] = str(metadata.get('meta_data_picture'))
    return JsonResponse(metadata)

def getMetaMainDataTag(request, id):
    metadata = model_to_dict(MetaData_Main.objects.get(nfc_tag=id))
    metadata['meta_data_picture'] = str(metadata.get('meta_data_picture'))
    return JsonResponse(metadata)


def updateMetaMainData(request, id):
    try:
        content = json.loads(request.POST.get('content'))
        metaData = MetaData_Main.objects.get(id=id)
        metaData.contacts = content['contacts']
        metaData.equipment_name = content['equipmentName']
        metaData.expected_service = content['expectedService']
        metaData.latest_service = content['latestService']
        metaData.latitude = content['latitude']
        metaData.legit = content['legal']
        metaData.longitude = content['longitude']
        metaData.nfc_tag = content['nfcTag']
        metaData.service_interval = content['serviceInterval']
        metaData.technical_category = content['technical']
        metaData.reminder_month = content['reminderMonth']
        metaData.reminder_week = content['reminderWeek']
        metaData.reminder_flag = '0'
        metaData.save()
        metaData.meta_data_picture.save(
            str(metaData.meta_data_picture), request.FILES['cover'])
        data = {"success": "false"}
    except:
        data = {"success": "true"}

    return JsonResponse(data)

def updateMetaMainDataLocation(request):
    print(request)
    # try:
    id = request.POST["id"]
    metaData = MetaData_Main.objects.get(id=id)
    metaData.latitude = request.POST['latitude']
    metaData.longitude = request.POST['longitude']
    metaData.save()
    data = {"success": "true"}
    # except:
    #     data = {"success": "faluse"}

    return JsonResponse(data)


def deleteMetaMainData(request, id):
    metaData = MetaData_Main.objects.get(id=id)
    if metaData:
        metaData.delete()
        MetaData_Archive.objects.create(
            meta_data_picture=metaData.meta_data_picture,
            technical_category=metaData.technical_category,
            equipment_name=metaData.equipment_name,
            nfc_tag=metaData.nfc_tag,
            service_interval=metaData.service_interval,
            legit=metaData.legit,
            expected_service=metaData.expected_service,
            latest_service=metaData.latest_service,
            contacts=metaData.contacts,
            longitude=metaData.longitude,
            latitude=metaData.latitude
        )
        return JsonResponse({'success': 'true'})
    else:
        return JsonResponse({'success': 'false'})


def getMetaActivity(request, id):
    try:
        datas = MetaData_Activity.objects.filter(equipment_name=id).all()
        serialized_obj = serializers.serialize('json', datas)
        return JsonResponse(serialized_obj, safe=False)
    except:
        return JsonResponse({'success': 'false'})


def getMetaActivityService(request, id):
    try:
        datas = (MetaData_Activity.objects.filter(equipment_name=id).all()).filter(service_repair='Service').all()
        serialized_obj = serializers.serialize('json', datas)
        return JsonResponse(serialized_obj, safe=False)
    except:
        return JsonResponse({'success': 'false'})


def getMetaArchiveDatas(request):
    metaDatas = MetaData_Archive.objects.all()
    data_list = []
    for metaData in metaDatas:
        item = model_to_dict(metaData)
        if (item.get('meta_data_picture')):
            item['meta_data_picture'] = str(item.get('meta_data_picture'))
        data_list.append(item)

    return JsonResponse(data_list, safe=False)


def getUserByID(request, id):
    user = model_to_dict(User.objects.get(user_name=id))
    return JsonResponse(user)

##################### Finish MetaMainData #############################

###### Maintenance start ###############

def getMaintenance(request):
    metaDatas = MetaData_Activity.objects.all()
    data_list = []
    for metaData in metaDatas:
        item = model_to_dict(metaData)
        data_list.append(item)

    return JsonResponse(data_list, safe=False)


def addMataArchive(request):
    try:
        MetaData_Activity.objects.create(
            equipment_name=request.POST['equipment_name'],
            service_repair=request.POST['service_repair'],
            date=request.POST['date'],
            due_time=request.POST['due_time'],
            serviced_by=request.POST['serviced_by'],
            comment=request.POST['comment'],
        )
        data = {"success": "true"}
    except:
        data = {"success": "false"}

    return JsonResponse(data)

# Technical Category


def getTechnicalCategory(request):
    categories = TechnicalCatergory.objects.all()
    data_list = []
    for category in categories:
        item = model_to_dict(category)
        data_list.append(item)

    return JsonResponse(data_list, safe=False)


def sendmail(user_name, user_email, reset_time, reset_id):
    routing_url = "http://localhost:8080/resetpassword?id=" + reset_id
    ctx = {
        'user': user_name,
        'reset_time': reset_time,
        'reset_url': routing_url
    }
    message = get_template('mail.html').render(ctx)
    msg = EmailMessage(
        'Subject',
        message,
        'norepleymaintenance@hotmail.com',
        [user_email],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    return HttpResponse('Mail successfully sent')

# Email Reset


def resetEmail(request):
    if request.method == "POST":
        email = json.loads(request.body.decode('utf-8'))
    try:
        user = get_object_or_404(User, email=email)
        newDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        newDate = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(20))
        user.reset_time = newDate
        user.reset_id = result_str
        user.save()
        sendmail(user.name, user.email, newDate, result_str)
        data = {
            'email': user.email
        }
    except:
        data = {
            'email': '',
        }

    return JsonResponse(data)


def checkResetID(request):
    if request.method == "POST":
        reset_id = json.loads(request.body.decode('utf-8'))
    try:
        user = get_object_or_404(User, reset_id=reset_id)
        current = datetime.now().timestamp()
        history = datetime.timestamp(user.reset_time)
        difference = (current - history)/3600
        if (difference < 24):
            data = {
                'reset_id': user.reset_id
            }
        else:
            data = {
                'reset_id': '',
            }

    except:
        data = {
            'reset_id': '',
        }

    return JsonResponse(data)


def resetPassword(request):
    if request.method == "POST":
        userInfor = json.loads(request.body.decode('utf-8'))
        password = userInfor['user_email']
        reset_id = userInfor['reset_id']
    try:
        user = get_object_or_404(User, reset_id=reset_id)
        user.password = password
        user.save()
        data = {
            'reset_id': reset_id,
        }
    except:
        data = {
            'reset_id': '',
        }

    return JsonResponse(data)


def resetEmailMobile(request):
    email = request.POST['email']
    try:
        user = get_object_or_404(User, email=email)
        newDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        newDate = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(20))
        user.reset_time = newDate
        user.reset_id = result_str
        user.save()
        sendmail(user.name, user.email, newDate, result_str)
        data = {
            'email': user.email
        }
    except:
        data = {
            'email': '',
        }
    return JsonResponse(data)