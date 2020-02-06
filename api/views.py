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
    u = authenticate(username = username , password = password)
    if u:
        user_obj = User.objects.get(username = username)
        userDetais_obj = UserDetails.objects.get(user = user_obj.id)
        data = {}
        data['username'] = user_obj.username
        data['name'] = user_obj.first_name + ' '+ user_obj.last_name
        data['email'] = user_obj.email
        data['image_url'] = userDetais_obj.pic.url
        data['org_id']  = userDetais_obj.org_id_id
        data['phone'] = userDetais_obj.phone
        data = json.dumps(data)
        return JsonResponse({'status' : 200,'data' : data})
        # user_obj = UserDetails.objects.get(user = u )
        # if user_obj.privilege == 2 :
        #     return JsonResponse({'status' : 200})
        # else:
        #     return JsonResponse('status')
    else:
        return JsonResponse({'status' : 300})


@csrf_exempt
def get_candidates(request):
    id  = (request.POST.get('org_id'))
    print(id)
    user_obj = UserDetails.objects.filter(org_id = Organisation.objects.get(id = id)).filter(privilege = 3)
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
    return JsonResponse({'status': 200, 'data': user_list})

@csrf_exempt
def get_analytics(request):
    username = request.POST.get('email')
    type = request.POST.get('type')
    # print(username)
    user_obj = User.objects.get(username = username)
    user_details_obj = UserDetails.objects.get(user = user_obj)
    org_id = user_details_obj.org_id_id
    print(org_id)
    result = get_anlytics_data(request , user_obj.id , org_id , type )
    return JsonResponse({'status' : 200 , 'data': result })



def get_anlytics_data(request ,id , org_id ,  type=None , camera_id = None ):
    user_obj = User.objects.get(id=id)
    # analytic_obj = Analytics.objects.filter(timestamp__month= 2 , timestamp__year = 2020)
    # print(analytic_obj)
    time_list = []
    count_list = []
    # print(id , type)
    print(camera_id , org_id , type)
    if camera_id is None:
        camera_obj = Camera.objects.filter(org_id = Organisation.objects.get(id = org_id)).first()
        camera_name = camera_obj.name
    else:
        camera_obj = Camera.objects.get(name=camera_id ,org_id = Organisation.objects.get(id=org_id) )
        camera_name = camera_id
    print(camera_obj.id)
    # print(camera_obj.name)
    # analytics_obj = Analytics.objects.all()
    # for analytics in analytics_obj:
    #     print('\n\n')
    #     print(analytics.timestamp)
    #     print(analytics.camera_id_id)
    #     print(analytics.user_id)

    if(type is None or type =='Last 7 days'):
        print('Last 7 days')
        no_of_days = 7
        today = timezone.now().date()
        first_date = today - datetime.timedelta(days=no_of_days - 1)
        for i in range(no_of_days):
            print(first_date)
            analytic_obj = Analytics.objects.filter(user=user_obj , timestamp__date = first_date ,camera_id = camera_obj)
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
            # if(first_date.month < 10):
            #     month = str('0'+str(first_date.month))
            # else:
            #     month = first_date.month
            year = first_date.year
            print(month , year)
            # print(month)
            analytic_obj = Analytics.objects.filter(user=user_obj,  timestamp__month=month, timestamp__year=year , camera_id = camera_obj)
            print(analytic_obj)
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
            if(hour < 10):
                hour = str('0' + str(first_date.hour))
            print(hour , first_date.date())
            # print(datetime.datetime.combine(first_date.date(), datetime.time(00,00,00,000000)))
            analytic_obj = Analytics.objects.filter(user=user_obj , timestamp__hour = first_date.hour ,
                                            timestamp__date = first_date.date() ,camera_id = camera_obj)
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

