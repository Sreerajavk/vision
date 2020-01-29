import string

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.utils.crypto import get_random_string

from .models import *

# Create your views here.

#for redirect to dashboard
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request , 'home.html',{})

def get_pic(request):
    user = User.objects.get(username=request.user)
    userDetails_obj = UserDetails.objects.get(user=user.id)
    pic = userDetails_obj.pic
    return pic
#the dashboard page
@login_required
def dashboard(request):
    return render(request , 'dashboard.html' , {'pic' : get_pic(request) })

@csrf_exempt
def add_organisation(request):
    if (request.method == 'POST'):
        org_name = request.POST.get('org_name')
        location = request.POST.get('location')
        org_obj = Organisation.objects.create(name = org_name , address = location)
        org_obj.save()
        print(org_obj.id)
        return JsonResponse({'id': org_obj.id})

@csrf_exempt
def org_signup(request):
    print('sd')
    if (request.method == 'POST'):
        print('in post')
        org_id = request.POST.get('org_id')
        # location = request.POST.get('location')
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        phone_no = request.POST.get('phone_no')
        image = request.FILES.get('image')
        #creating organisation
        print(username , password)

        # print(org_name , location)
        # print( org_id , email)
        # print(image)
        org_obj = Organisation.objects.get(id = org_id)
        try:
            user_obj = User.objects.create(username = username , password = password , first_name = first_name , last_name = last_name , email = email)
            user_obj.save()
            user_details_obj = UserDetails.objects.create(user = user_obj , org_id = org_obj , phone = phone_no , pic = image , privilege = 1)
            user_obj.save()
            return JsonResponse({'status': 200})

        except:
            return JsonResponse({'status': 300})





    return render(request, 'OrgSignup.html', {})

@csrf_exempt
def login_fn(request):

    if(request.method == 'POST'):
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username , password)
        # try:
        # u = authenticate(username = username , password = password )
        u = User.objects.filter(username = username , password = password)
        # print(u)
        print(u)
        if u:
            # user = User.objects.get(username = u )
            u = u.first()
            user_obj = UserDetails.objects.get(user = u.id )
            if(user_obj.privilege == 1 ):
                login(request , u)
                return JsonResponse({'status' : 200 })
            else:
                return JsonResponse({'status': 300})
        else:
            return JsonResponse({'status': 500})


    return render(request , 'Login.html' , {})

@csrf_exempt
@login_required
def add_staff(request):
    if(request.method == 'POST'):
        # print(request.POST)
        email = request.POST.get('email')
        print(request.user)
        u = User.objects.get(username = request.user )
        print(u.id)
        user_obj = UserDetails.objects.get(user=u.id)

        # send_mail(
        #     'Subject here',
        #     'Here is the message.',
        #     'sreerajavk@gmail.com',
        #     [email],
        #     fail_silently=False,
        # )
        # create_token()
        current_site = get_current_site(request)
        subject, to = 'Email Verification | Secure Vision', email
        token = create_token()
        obj = StaffVerification.objects.create(token = token , email = email , visited = False)
        obj.save()
        html_content = get_template('email.html').render(dict({
            'name': email,
            'domain': current_site.domain,
            'token': token,
            'org_id' : user_obj.org_id_id
        }))

        email = EmailMessage(subject, html_content, to=[to])
        email.content_subtype = "html"  # Main content is now text/html
        email.send()
        return  JsonResponse({'status' : 200})


    # print(get_pic(request))
    return render(request , 'AddStaff.html' , {'pic' : get_pic(request)})

def create_token():

    num = StaffVerification.objects.aggregate(Max('id'))['id__max']
    if(num is None):
        num = 1
    else:
        num +=1
    unique_id = get_random_string(length = 30 , allowed_chars=string.ascii_letters)
    unique_id += str(num)
    print(unique_id)
    return unique_id


def verify_staff(request , token , email ,org_id):

    verify_obj = StaffVerification.objects.filter(token = token , email = email )
    # print(type (verify_obj))
    if verify_obj:
        verify_obj = verify_obj.first()
        if(verify_obj.visited):
            return redirect('/login')
        else:
            verify_obj.visited = True
            verify_obj.save()
            return redirect('/staff-signup/?email='+email+'&org_id=' + org_id )

    else:
        return render(request , '404.html')


def error_page(request ):
    return render(request , '404.html')

def staff_signup(request):
    # print(request.META.get('HTTP_REFERER'))


    if(request.method == 'POST'):

        org_id = request.POST.get('org_id')
        # location = request.POST.get('location')
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        phone_no = request.POST.get('phone_no')
        image = request.FILES.get('image')
        # creating organisation

        # print(org_name , location)
        # print( org_id , email)
        # print(image)
        org_obj = Organisation.objects.get(id=org_id)
        try:
            user_obj = User.objects.create(username=username, password=password, first_name=first_name,
                                           last_name=last_name, email=email)
            user_obj.save()
            user_details_obj = UserDetails.objects.create(user=user_obj, org_id=org_obj, phone=phone_no, pic=image,
                                                          privilege=2)
            user_obj.save()
            return JsonResponse({'status': 200})

        except:
            return JsonResponse({'status': 300})

    email = request.GET.get('email')
    org_id = request.GET.get('org_id')
    # print(email)
    user_obj  = User.objects.filter(email = email)
    print(user_obj)
    if user_obj:
        return  render(request , 'staffSignup.html' , {'email': email , 'org_id':org_id})
    else:
        return render(request , '404.html')

def logout_fn(request):
    logout(request)
    return redirect('/login/')