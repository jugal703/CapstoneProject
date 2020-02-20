from django.shortcuts import render, redirect
from django.views import View

import ADTAA.models as ADTAA_models


def index(request):
    return render(request, 'ADTAA/index.html')


def root_home_page(request):
    return render(request, 'ADTAA/rootHome.html')


def admin_home_page(request):
    return render(request, 'ADTAA/adminHome.html')


def scheduler_home_page(request):
    return render(request, 'ADTAA/schedulerHome.html')


def password_page(request):
    return render(request, 'ADTAA/password.html')


def setup_instructor(request):
    return render(request, 'ADTAA/instrSetup.html')


def setup_classes(request):
    return render(request, 'ADTAA/classSetup.html')


class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ADTAA/reg.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)
        user_type = request.POST.get('userType', None)
        first_name = request.POST.get('firstName', None)
        last_name = request.POST.get('lastName', None)
        sec_question1 = request.POST.get('question1', None)
        sec_question2 = request.POST.get('question2', None)

        if not email or not first_name or not last_name or not sec_question1 or not sec_question2:
            context = {
                'error': 'Must Pass In Every Verify.'
            }
            return render(request, 'ADTAA/reg.html', context=context)

        new_user = ADTAA_models.BaseUser(
            user_type=user_type,
            username=email,
            first_name=first_name,
            last_name=last_name,
            sec_question1=sec_question1,
            sec_question2=sec_question2,
        )

        new_user.save()

        return redirect('/ADTAA')
