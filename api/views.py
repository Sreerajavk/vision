import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
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
        data = json.dumps(data)
        return JsonResponse({'status' : 200,'data' : data})
        # user_obj = UserDetails.objects.get(user = u )
        # if user_obj.privilege == 2 :
        #     return JsonResponse({'status' : 200})
        # else:
        #     return JsonResponse('status')
    else:
        return JsonResponse({'status' : 300})
