import calendar
import string
import datetime
from django.utils  import timezone

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.db.models import Max
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.utils.crypto import get_random_string

from .forms import ImageForm
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
            user_obj = User.objects.create_user(username = username , password = password , first_name = first_name , last_name = last_name , email = email)
            user_obj.save()
            user_details_obj = UserDetails.objects.create(user = user_obj , org_id = org_obj , phone = phone_no , pic = image , privilege = 1)
            user_obj.save()
            return JsonResponse({'status': 200})

        except:
            return JsonResponse({'status': 300})





    return render(request, 'OrgSignup.html', {})

@csrf_exempt
def login_fn(request):

    if(request.user.is_authenticated):
        return redirect('/dashboard/')

    if(request.method == 'POST'):
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username , password)
        # try:
        u = authenticate(username = username , password = password )
        # u = User.objects.filter(username = username , password = password)
        # print(u)
        print(u)
        if u:
            # print('sdf')
            # u = User.objects.filter(username=username)
            user_obj = User.objects.get(username = u )
            print(user_obj.id)
            # u = u.first()
            userdetails_obj = UserDetails.objects.get(user = user_obj.id )
            if(userdetails_obj.privilege == 1 ):
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
        # username = request.POST.get('username')
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
            user_obj = User.objects.create(username=email, password=password, first_name=first_name,
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

@login_required
def upload_images(request):
    # ImageFormSet = modelformset_factory(CandidatePics , form=ImageForm, extra=2)

    if(request.method == 'POST'):
        print(request.POST)
        image = request.FILES.get('images')
        user_id = request.POST.get('user_id')
        edit = request.POST.get('edit')
        user_obj  = User.objects.get(id = user_id)
        pic_obj = CandidatePics.objects.create(user = user_obj , images = image )
        user_details_obj = UserDetails.objects.get(user = user_obj)
        print(user_details_obj.pic)
        if(user_details_obj.pic == ''):
            user_details_obj.pic = image
            user_details_obj.save()
        pic_obj.save()
        return JsonResponse({'status' : 200 , 'edit' : edit})
    return render(request , 'AddCandidate.html' , { 'pic' : get_pic(request)} )

@login_required
@csrf_exempt
def add_candidates(request):

    if(request.method == 'POST'):
        org_id = request.POST.get('org_id')
        # location = request.POST.get('location')
        # email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # password = request.POST.get('password')
        phone_no = request.POST.get('phone')

        print(org_id , username , first_name , last_name , phone_no)

        try:
            org_obj = Organisation.objects.get(id = org_id)
            u = User.objects.create_user(username = username , password = 'password' , first_name = first_name,last_name = last_name )
            user_obj = UserDetails.objects.create(user = u , org_id = org_obj , phone = phone_no , privilege = 3)
            return JsonResponse({'status': 200 , 'user_id' : u.id })
        except:
            return JsonResponse({'status' : 300})

    user_obj = UserDetails.objects.get(user = request.user)
    status = request.GET.get('status')
    print(status)
    return render(request ,'AddCandidate.html' , {'pic' : get_pic(request) ,'org_id' : user_obj.org_id , 'status': status })


#delete and edit candidates and staff
@login_required
@csrf_exempt
def manage(request):

    if(request.method == 'POST'):
        org_id = request.POST.get('org_id')
        option = request.POST.get('option')
        print(org_id , option)
        data = {}
        if(int(option) == 0 ):
            staff_obj = UserDetails.objects.filter(privilege = 2 , org_id = org_id)
            for staff in staff_obj:
                dic = {}
                dic['first_name'] = staff.user.first_name
                dic['last_name'] = staff.user.last_name
                dic['username'] = staff.user.username
                dic['email'] = staff.user.email
                dic['phone'] = staff.phone
                dic['image_url'] =staff.pic.url
                data[staff.user.id] = dic
            flag = 1
                # print(dic)
            print(data)
        else:
            staff_obj = UserDetails.objects.filter(privilege=3, org_id=org_id)
            for staff in staff_obj:
                dic = {}
                dic['first_name'] = staff.user.first_name
                dic['last_name'] = staff.user.last_name
                dic['username'] = staff.user.username
                # dic['email'] = staff.user.email
                dic['phone'] = staff.phone
                dic['image_url'] = staff.pic.url
                data[staff.user.id] = dic
            flag=0
                # print(dic)
            print(data)
        return JsonResponse({'data': data , 'status': 200 , 'flag': flag})


    user_obj = UserDetails.objects.get(user = request.user)
    status = request.GET.get('status')
    return render(request , 'Manage.html' , {'pic' : get_pic(request),'org_id': user_obj.org_id , 'status': status})



@csrf_exempt
def delete_staff(request):

    if(request.method == 'POST'):
        print(request.POST)
        id = request.POST.get('user_id')
        type = request.POST.get('type')
        org_id = request.POST.get('org_id')
        # print(id , org_id , type)
        User.objects.filter(id = id).delete()
        org_obj = Organisation.objects.get(id = org_id )
        if(int(type) == 0 ):
            user_obj = UserDetails.objects.filter(org_id = org_obj , privilege = 3)
        else:
            user_obj = UserDetails.objects.filter(org_id=org_obj, privilege=2)
        length = user_obj.count()
        print(length)
        return JsonResponse({'status': 200 , 'id' : id , 'length' : length})

@login_required
def edit_candidate(request,id):

    if(request.method == 'POST'):
        # print('In post')
        # org_id = request.POST.get('org_id')
        # location = request.POST.get('location')
        # email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # password = request.POST.get('password')
        phone_no = request.POST.get('phone')
        id = request.POST.get('id')

        user_obj = User.objects.get(id = id)
        user_details_obj = UserDetails.objects.get(user = user_obj)
        user_details_obj.phone = phone_no
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.save()
        user_details_obj.save()
        pic_obj = CandidatePics.objects.filter(user = user_obj)
        pic_list = []
        for pic in pic_obj:
            dic = {}
            dic['id'] = pic.id
            dic['image_url'] = pic.images.url
            pic_list.append(dic)
        return JsonResponse({'status': 200 , 'pic_list' : pic_list , 'name': first_name+' ' + last_name , 'user_id':id})


    print(id)
    # return HttpResponse('sldfkjsdlkf')
    user = User.objects.filter(id = id )
    if user:
        user_obj = UserDetails.objects.get(user = user.first())
        user = user.first()
        dic = {}
        dic['first_name'] = user.first_name
        dic['last_name'] = user.last_name
        dic['username'] = user.username
        # dic['email'] = user.user.email
        dic['id'] = id
        dic['org_id'] = user_obj.org_id_id
        dic['phone'] = user_obj.phone
        return render(request, 'EditCandidates.html', {'data' : dic , 'pic':get_pic(request)})
    else:

        return render(request , '404.html' , {})


@login_required
def delete_images(request):

    if(request.is_ajax()):
        id = request.POST.get('id')
        pic_obj = CandidatePics.objects.get(id = id)
        pic_obj.delete()
        return JsonResponse({'status': 200  , 'id' : id})

@login_required
def analytics(request):

    user_list = get_user_data(request)
    # user_obj = User.objects.get(username  = request.user)
    # org_id = UserDetails.objects.get(user = user_obj).org_id_id
    # org_obj = Organisation.objects.get(id = org_id)
    # user_details_obj = UserDetails.objects.exclude(user = request.user).filter(org_id = org_obj)
    # user_list = []
    # count = 1
    # for u in user_details_obj:
    #     dic = {}
    #     dic['name'] = u.user.first_name + ' ' + u.user.last_name
    #     if(u.privilege == 3):
    #         type = "Candidate"
    #     else:
    #         type = "Staff"
    #     dic['privilege']  = type
    #     dic['image_url'] = u.pic.url
    #     dic['id'] = u.user.id
    #     dic['count'] = count
    #     count +=1
    #     user_list.append(dic)
    return render(request , 'Analytics.html' , {'pic' : get_pic(request) , 'user_list' : user_list})

@login_required
@csrf_exempt
def filter_type(request):

    if(request.is_ajax()):
        option = request.POST.get('option')
        print(option)
        user_list = get_user_data(request , option = option)
        print(user_list)
        return JsonResponse({'status': 200 , 'user_list' : user_list})




def get_user_data(request , option=None):
    print(option)
    user_obj = User.objects.get(username=request.user)
    org_id = UserDetails.objects.get(user=user_obj).org_id_id
    org_obj = Organisation.objects.get(id=org_id)
    user_details_obj = UserDetails.objects.exclude(user=request.user).filter(org_id=org_obj)
    user_list = []
    count = 1
    if(option == '0'):
        user_details_obj = user_details_obj.filter(privilege = 2)
    elif(option == '1'):
        user_details_obj = user_details_obj.filter(privilege = 3)
    else:
        pass
    for u in user_details_obj:
        dic = {}
        dic['name'] = u.user.first_name + ' ' + u.user.last_name
        if(u.privilege == 3):
            type = "Candidate"
        else:
            type = "Staff"
        dic['privilege']  = type
        dic['image_url'] = u.pic.url
        dic['id'] = u.user.id
        dic['count'] = count
        count +=1
        user_list.append(dic)
    return user_list


def get_anlytics_data(request ,id ,  type=None):
    user_obj = User.objects.get(id=id)
    # analytic_obj = Analytics.objects.filter(timestamp__month= 2 , timestamp__year = 2020)
    # print(analytic_obj)
    time_list = []
    count_list = []
    # print(id , type)
    #
    analytics_obj = Analytics.objects.all()
    for analytics in analytics_obj:
        print('\n\n')
        print(analytics.timestamp)
        print(analytics.camera_id_id)
        print(analytics.user_id)

    if(type is None or type =='day'):
        no_of_days = 7
        today = timezone.now().date()
        first_date = today - datetime.timedelta(days=no_of_days - 1)
        for i in range(no_of_days):
            print(first_date)
            analytic_obj = Analytics.objects.filter(user=user_obj , timestamp__range = (datetime.datetime.combine(first_date, datetime.time.min),
                            datetime.datetime.combine(first_date, datetime.time.max)))
            print(analytic_obj)
            count = analytic_obj.count()
            time_list.append(first_date.strftime("%d %b"))
            count_list.append(count)
            first_date += datetime.timedelta(days =1)
    elif(type == 'month'):
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
            analytic_obj = Analytics.objects.filter(user=user_obj,  timestamp__month=month, timestamp__year=year)
            print(analytic_obj)
            count = analytic_obj.count()
            time_list.append(first_date.strftime("%b %Y"))
            count_list.append(count)
            first_date = monthdelta(first_date , 1)
    else:
        print('in hour')
        no_of_hours = 10
        today = timezone.now()
        print(today)
        first_date = today - datetime.timedelta(hours=8)
        print(first_date)
        # print((first_date.hour))
        for i in range(no_of_hours):
            hour = first_date.hour
            if(hour < 10):
                hour = str('0' + str(first_date.hour))
            print(hour , first_date.date())
            # print(datetime.datetime.combine(first_date.date(), datetime.time(00,00,00,000000)))
            analytic_obj = Analytics.objects.filter(user=user_obj , timestamp__hour = first_date.hour , timestamp__date = first_date.date() )
            count = analytic_obj.count()
            time_list.append(first_date.strftime("%I %p"))
            count_list.append(count)
            first_date += datetime.timedelta(hours=1)

    print(time_list , count_list)

    return [time_list , count_list]





@login_required
@csrf_exempt
def get_analytics(request):

    if(request.is_ajax()):
        id = request.POST.get('id')
        type = request.POST.get('type')
        # print(id , type)
        user_obj = User.objects.get(id = id)
        data = {}
        data['id'] = id
        data['name'] = user_obj.first_name + ' ' + user_obj.last_name
        result = get_anlytics_data(request , id , type=type)
        return JsonResponse({'status': 200 , 'count_list': result[1] , 'time_list' : result[0] ,'data' :data})




def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d,month=m, year=y)