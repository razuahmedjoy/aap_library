from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth import authenticate, login,logout


from django.contrib.auth.models import User
from bookstore.models import *

import random
import requests


def send_sms(contact_no, message):

    url = f"http://66.45.237.70/api.php?username={settings.SMS_API_USERNAME}&password={settings.SMS_API_PASSWORD}&number={contact_no}&message={message}"

    payload = {}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        responsetxt = response.text[:4]
    except:
        responsetxt = None

    return responsetxt


def register(request):
    error = ""
    context = {
        "title": "Create Your Account",
        "error": error,
    }

    if request.method == 'POST':
        serverotp = request.POST.get("serverotp")
        userotp = request.POST.get("userotp")
        contact_no = request.POST.get("contact_no")
        if serverotp == userotp:

            context["contact_no"] = contact_no
            return render(request, "bookstore/createaccount.html", context)

        else:
            context["error"] = "Invalid OTP, Please enter correct OTP"
            context["otp_sent"] = True
            context["serverotp"] = serverotp
            context["contact_no"] = contact_no

    if request.method == 'GET':
        if "contact_no" in request.GET:
            contact_no = request.GET.get("contact_no")
            
            if len(contact_no) == 11:
                try:
                    user_exist = User.objects.get(username=contact_no)
                    context['error'] = "Another account already exists with this number, Login with that account"
                    return render(request, "bookstore/register.html", context)
                except:
                    pass
                    
                contact_no_for_sms = "88"+str(contact_no)
                otp = random.randint(100000, 999999)
                message = f"Your Academic Admission Library OTP is {otp}"

                sms_response = send_sms(contact_no_for_sms, message)

                if sms_response == '1101':
                    context['serverotp'] = otp
                    context['contact_no'] = contact_no
                    context['otp_sent'] = True

                else:
                    context['error'] = "Something error in sms provider"
            else:
                context['error'] = "Contact No. Should be 11 Digits (01234567899)"

    return render(request, 'bookstore/register.html', context)


def createaccount(request):
    context = {}
    if request.method == 'POST':
        contact_no = request.POST.get('contactno')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # creating user
        main_user = User.objects.create_user(
            username=contact_no, password=password, first_name=username)
        main_user.save()

        # creating customer account
        customer = Customers(user=main_user, name=username,
                             contact_no=contact_no)
        customer.save()

        context['success'] = "Your account succefully created. Login Now using the contact no and password"
        context['title'] = "Login"

        return render(request, 'bookstore/login.html', context)

        return HttpResponse({"data": request.POST})
    else:
        return HttpResponseRedirect('/')


def passwordresetView(request):
    error = ""
    context = {
        "title": "",
        "error": error,
        "reset" : True,
    }

    if request.method == 'POST':
        serverotp = request.POST.get("serverotp")
        userotp = request.POST.get("userotp")
        contact_no = request.POST.get("contact_no")
        if serverotp == userotp:

            context["contact_no"] = contact_no
            return render(request, "bookstore/createaccount.html", context)

        else:
            context["error"] = "Invalid OTP, Please enter correct OTP"
            context["otp_sent"] = True
            context["serverotp"] = serverotp
            context["contact_no"] = contact_no

    if request.method == 'GET':
        if "contact_no" in request.GET:
            contact_no = request.GET.get("contact_no")
            
            if len(contact_no) == 11:
                try:
                    User.objects.get(username=contact_no)     
                    contact_no_for_sms = "88"+str(contact_no)
                    otp = random.randint(100000, 999999)
                    message = f"Your Academic Admission Library OTP is {otp}"

                    sms_response = send_sms(contact_no_for_sms, message)

                    if sms_response == '1101':
                        context['serverotp'] = otp
                        context['contact_no'] = contact_no
                        context['otp_sent'] = True

                    else:
                        context['error'] = "Something error in sms provider"
                except:
                    context['error'] = "No Account is Registered with this number"



            else:
                context['error'] = "Contact No. Should be 11 Digits (01234567899)"



    return render(request, 'bookstore/register.html', context)



 
def login_view(request):

    if request.user.is_authenticated:
        return redirect('/')
    context = {}

    if request.method == 'POST':
        username = request.POST['contact_no']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST['next'])
            else:
                return redirect("/")
        else:
            context['error'] = "Wrong Number or Password"

    return render(request, 'bookstore/login.html', context)


def LogoutView(request):
    logout(request)
    return redirect('/')













def resetpassView(request):
    context = {}
    if request.method == 'POST':
        contact_no = request.POST.get('contactno')
        password = request.POST.get('password')

        user = User.objects.get(username=contact_no)

        user.set_password(password)
        user.save()

        context['success'] = "Your Password Has Been Succesfully Reset, Login With Your New Password"
        context['title'] = "Login"

        return render(request, 'bookstore/login.html', context)

        
    else:
        return HttpResponseRedirect('/')










