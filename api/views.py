import calendar
import datetime
import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from dashboard.models import  *

@csrf_exempt
def login_fn(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username , password)
    u = authenticate(username = username , password = password)
    if u:
        print('LOgged In')
        user_obj = User.objects.get(username = username)
        userDetais_obj = UserDetails.objects.get(user = user_obj.id)
        data = {}
        data['username'] = user_obj.username
        data['name'] = user_obj.first_name + ' '+ user_obj.last_name
        data['email'] = user_obj.email
        data['image_url'] = userDetais_obj.pic.url
        data['org_id']  = userDetais_obj.org_id_id
        data['phone'] = userDetais_obj.phone

        #getting organisation details
        data['api_key'] = userDetais_obj.org_id.api_key
        data = json.dumps(data)
        return JsonResponse({'status' : 200,'data' : data})
        # user_obj = UserDetails.objects.get(user = u )
        # if user_obj.privilege == 2 :
        #     return JsonResponse({'status' : 200})
        # else:
        #     return JsonResponse('status')
    else:
        print('Error')
        return JsonResponse({'status' : 300})


@csrf_exempt
def get_candidates(request):
    api_key  = request.POST.get('api_key')
    print(api_key)
    org_obj = Organisation.objects.get(api_key = api_key)
    user_obj = UserDetails.objects.filter(org_id = org_obj).filter(privilege = 3)
    user_list = []
    for user in user_obj:
        data = {}
        data['username'] = user.user.username
        data['name'] = user.user.first_name + ' ' + user.user.last_name
        # data['email'] = user_obj.email
        data['image_url'] = user.pic.url
        # data['org_id'] = userDetais_obj.org_id_id
        # data['phone'] = userDetais_obj.phone
        user_list.append(data)
    data = json.dumps(user_list)
    camera_list = []
    camera_list.append('All Cameras')
    camera_obj = Camera.objects.filter(org_id=org_obj)
    for camera in camera_obj:
        camera_list.append(camera.name)
    return JsonResponse({'status': 200, 'data': user_list , 'camera_list' : camera_list})

@csrf_exempt
def get_analytics(request):
    username = request.POST.get('email')
    api_key = request.POST.get('api_key')
    type = request.POST.get('type')
    camera_id = request.POST.get('camera_obj')
    print(username , api_key , type)
    user_obj = User.objects.get(username = username)
    user_details_obj = UserDetails.objects.get(user = user_obj)
    org_id = user_details_obj.org_id_id
    # print(org_id)
    result = get_anlytics_data(request , user_obj.id , api_key , camera_id , type)
    return JsonResponse({'status' : 200 , 'data': result })


@csrf_exempt
def get_anlytics_data(request ,id , api_key , camera_id  , type=None  ):
    user_obj = User.objects.get(id=id)
    time_list = []
    count_list = []
    # print(id , type)
    print('In getanalytics')
    print(camera_id , api_key , type)
    org_obj = Organisation.objects.get(api_key=api_key)
    camera_status = 0
    if camera_id == 'All Cameras':
        print('sdfsjdflksdjflk')
        camera_name = "All cameras"
        camera_status=1
    else:
        camera_obj = Camera.objects.get(name=camera_id ,org_id = org_obj.id )
        camera_name = camera_id

    if(type is None or type =='Last 7 days'):
        print('Last 7 days')
        no_of_days = 7
        today = timezone.now().date()
        first_date = today - datetime.timedelta(days=no_of_days - 1)
        for i in range(no_of_days):
            analytic_obj = Analytics.objects.filter(user=user_obj, timestamp__date=first_date)
            if(not camera_status):
                analytic_obj = Analytics.objects.filter(user=user_obj, timestamp__date=first_date, camera_id=camera_obj)
            print(analytic_obj)
            count = analytic_obj.count()
            time_list.append(first_date.strftime("%d %b"))
            count_list.append(count)
            first_date += datetime.timedelta(days =1)
    elif(type == 'Last 6 months'):
        print('Last 6 months')
        no_of_months = 6
        today = timezone.now().date()
        print(today.today())
        first_date = monthdelta(today.today() , -no_of_months)
        print(first_date)
        for i in range(no_of_months +1 ):
            month = first_date.month
            year = first_date.year
            analytic_obj = Analytics.objects.filter(user=user_obj, timestamp__month=month, timestamp__year=year)
            if(not camera_status):
                analytic_obj = Analytics.objects.filter(user=user_obj, timestamp__month=month, timestamp__year=year,
                                                        camera_id=camera_obj)
            count = analytic_obj.count()
            time_list.append(first_date.strftime("%b"))
            count_list.append(count)
            first_date = monthdelta(first_date , 1)
    else:
        print('in hour')
        no_of_hours = 8
        today = timezone.now()
        print(today)
        first_date = today - datetime.timedelta(hours=7)
        print(first_date)
        # print((first_date.hour))
        for i in range(no_of_hours):
            hour = first_date.hour
            analytic_obj = Analytics.objects.filter(user=user_obj, timestamp__hour=first_date.hour,
                                                    timestamp__date=first_date.date())
            if(not camera_status):
                analytic_obj = Analytics.objects.filter(user=user_obj, timestamp__hour=first_date.hour,
                                                        timestamp__date=first_date.date(), camera_id=camera_obj)
            count = analytic_obj.count()
            time_list.append(first_date.strftime("%I%p"))
            count_list.append(count)
            first_date += datetime.timedelta(hours=1)

    print(time_list , count_list)

    return [time_list , count_list , camera_name]


def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d,month=m, year=y)

