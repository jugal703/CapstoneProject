from django.contrib import auth
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test

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
                login(request, user)
                request.session['username'] = email
                return render(request, 'ADTAA/adminHome.html')
            if user.user_type == "scheduler":
                login(request, user)
                request.session['username'] = email
                return render(request, 'ADTAA/schedulerHome.html')
        else:
            context = {
                'error': 'No user exist, or wrong password'
            }
            return render(request, 'ADTAA/index.html', context=context)


def scheduler_check(user):
    user = ADTAA_models.BaseUser
    return user.user_type == 'scheduler'


def admin_check(user):
    user = ADTAA_models.BaseUser
    return user.user_type == 'admin'


def root_check(user):
    user = ADTAA_models.BaseUser
    return user.user_type == 'root'


def scheduler_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/ADTAA/'):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == "scheduler",
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/ADTAA/'):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == "admin",
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def root_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/ADTAA/'):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == "root",
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def admin_root_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/ADTAA/'):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == "root" or u.user_type == "admin",
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


@login_required
@root_required
def root_home_page(request):
    return render(request, 'ADTAA/rootHome.html')


@login_required
@admin_required
def admin_home_page(request):
    return render(request, 'ADTAA/adminHome.html')


@login_required
@scheduler_required
def scheduler_home_page(request):
    return render(request, 'ADTAA/schedulerHome.html')


def password_page(request):
    return render(request, 'ADTAA/password.html')


def password2_page(request):
    return render(request, 'ADTAA/password2.html')


@login_required
@admin_root_required
def setup_instructor(request):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    context = {
        'user': user.user_type
    }
    return render(request, 'ADTAA/instrSetup.html', context)


@login_required
@admin_root_required
def setup_classes(request):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    context = {
        'user': user.user_type
    }
    return render(request, 'ADTAA/classSetup.html', context)


@login_required(login_url='/ADTAA/')
def admin_nav(request):
    return render(request, 'ADTAA/adminNav.html')


@login_required(login_url='/ADTAA/')
def root_nav(request):
    return render(request, 'ADTAA/rootNav.html')


@login_required(login_url='/ADTAA/')
def scheduler_nav(request):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    context = {
        'user': user
    }
    return render(request, 'ADTAA/schedulerNav.html', context)


@login_required(login_url='/ADTAA/')
def edit_solutions(request):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    context = {
        'user': user.user_type
    }
    return render(request, 'ADTAA/editSolutions.html', context)


@login_required(login_url='/ADTAA/')
def generate_solutions(request):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    context = {
        'user': user.user_type
    }
    return render(request, 'ADTAA/generateSolutions.html', context)


class Register(View):
    form_class = ADTAA_forms.RegistrationForm

    def __init__(self):
        # Set registration_form for this instance to a new (and empty) instance of the
        # appropriate Form class for this View
        self.registration_form = self.form_class()

    def get(self, request, *args, **kwargs):
        # At this point, self.registration_form is a new instance of our form class and
        # we simply need to pass it to our template for rendering. We do that using a
        # context variable.
        context = {
            'registration_form': self.registration_form,
        }
        return render(request, 'ADTAA/reg.html',context)

    def post(self, request, *args, **kwargs):
        # Set registration_form for this instance to a new instance of the appropriate
        # Form class for this View based on the form that was POSTed to this function
        self.registration_form = self.form_class(request.POST)
        if not self.registration_form.is_valid():
            context = {
                'registration_form': self.registration_form,
            }
            return render(request, 'wordy_game_app/user_management/register.html', context)

        new_user = self.registration_form.save()
        request.session['new_username'] = new_user.username

        return redirect('/ADTAA')


def logout(request):
    auth.logout(request)
    return render(request, 'ADTAA/logout.html')


class PasswordPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ADTAA/password.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)
        sec_question1 = request.POST.get('secQuestion1', None)
        sec_question2 = request.POST.get('secQuestion2', None)

        if not email or not sec_question1 or not sec_question2:
            context = {
                'error': 'Must Pass In Every Verification.'
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
