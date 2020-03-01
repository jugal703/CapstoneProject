from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout

import ADTAA.models as ADTAA_models


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ADTAA/index.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        if not email or not password:
            context = {
                'error': 'Must Pass In Every Verify.'
            }
            return render(request, 'ADTAA/index.html', context=context)

        user = ADTAA_models.BaseUser.objects.get(username=email)

        if user.check_password(password):
            if user.user_type == "admin":
                return redirect('/ADTAA/adminHome')
            if user.user_type == "scheduler":
                return redirect('/ADTAA/schedulerHome')
        else:
            context = {
                'error': 'No user exist, or wrong password'
            }
            return render(request, 'ADTAA/index.html', context=context)


def root_home_page(request):
    return render(request, 'ADTAA/rootHome.html')


def admin_home_page(request):
    return render(request, 'ADTAA/adminHome.html')


def scheduler_home_page(request):
    return render(request, 'ADTAA/schedulerHome.html')


def setup_instructor(request):
    return render(request, 'ADTAA/instrSetup.html')

def setup_classes(request):
    return render(request, 'ADTAA/classSetup.html')

def edit_solutions(request):
    return render(request, 'ADTAA/editSolutions.html')

def generate_solutions(request):
    return render(request, 'ADTAA/generateSolutions.html')

def scheduler_nav(request):
    return render(request, 'ADTAA/schedulerNav.html')

def admin_nav(request):
    return render(request, 'ADTAA/adminNav.html')

def root_nav(request):
    return render(request, 'ADTAA/rootNav.html')

class Register(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'ADTAA/reg.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)
        user_type = request.POST.get('userType', None)
        password = request.POST.get('password', None)
        sec_question1 = request.POST.get('question1', None)
        sec_question2 = request.POST.get('question2', None)

        if not email or not password or not user_type or not sec_question1 or not sec_question2:
            context = {
                'error': 'Must Pass In Every Verify.'
            }
            return render(request, 'ADTAA/reg.html', context=context)

        new_user = ADTAA_models.BaseUser(
            user_type=user_type,
            username=email,
            sec_question1=sec_question1,
            sec_question2=sec_question2,
        )
        new_user.set_password(password)
        new_user.save()

        return redirect('/ADTAA')

<<<<<<< HEAD

class PasswordPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ADTAA/password.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)
        sec_question1 = request.POST.get('secQuestion1', None)
        sec_question2 = request.POST.get('secQuestion2', None)

        if not email or not sec_question1 or not sec_question2:
            context = {
                'error': 'Must Pass In Every Verify.'
            }
            return render(request, 'ADTAA/password.html', context=context)

        user = ADTAA_models.BaseUser.objects.all().filter(
            username=email,
            sec_question1=sec_question1,
            sec_question2=sec_question2
        ).count()
        if user:
            request.session['username'] = email
            return redirect('/ADTAA/password2')
        else:
            context = {
                'error': 'wrong answer'
            }
            return render(request, 'ADTAA/password.html', context=context)


class PasswordPage2(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ADTAA/password2.html')

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password', None)
        username = request.session.pop('username', '0')
        user = ADTAA_models.BaseUser.objects.get(username=username)
        user.set_password(password)
        user.save()
    
        return redirect('/ADTAA')
=======
def logout_view(request):
    logout(request)
    return redirect('/ADTAA')

>>>>>>> 6b37dbfbb10b9c516b8d47e582c6f7903579b463
