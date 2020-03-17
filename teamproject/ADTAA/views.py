from django.contrib import auth
from django.contrib.auth import login, REDIRECT_FIELD_NAME, get_user_model
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

import ADTAA.models as ADTAA_models
import ADTAA.forms as ADTAA_forms
from ADTAA.globals import raise_unexpected_error


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
            if user.isApproved == "yes":
                if user.user_type == "root":
                    login(request, user)
                    request.session['username'] = email
                    return render(request, 'ADTAA/rootHome.html')
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
                    'error': 'User Has Not Been Approved Yet'
                }
                return render(request, 'ADTAA/index.html', context=context)
        else:
            context = {
                'error': 'Username Or Password Is Incorrect'
            }
            return render(request, 'ADTAA/index.html', context=context)


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
        'user_type': user.user_type
    }
    return render(request, 'ADTAA/instrSetup.html', context)


@login_required
@admin_root_required
def setup_classes(request):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    context = {
        'user_type': user.user_type
    }
    return render(request, 'ADTAA/classSetup.html', context)


@login_required(login_url='/ADTAA/')
def admin_nav(request):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    context = {
        'user': user
    }
    return render(request, 'ADTAA/adminNav.html', context)


@login_required(login_url='/ADTAA/')
def root_nav(request):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    context = {
        'user': user
    }
    return render(request, 'ADTAA/rootNav.html', context)


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
        'user_type': user.user_type
    }
    return render(request, 'ADTAA/editSolutions.html', context)


@login_required(login_url='/ADTAA/')
def generate_solutions(request):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    context = {
        'user_type': user.user_type
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
        return render(request, 'ADTAA/reg.html', context)

    def post(self, request, *args, **kwargs):
        # Set registration_form for this instance to a new instance of the appropriate
        # Form class for this View based on the form that was POSTed to this function
        self.registration_form = self.form_class(request.POST)
        if not self.registration_form.is_valid():
            context = {
                'registration_form': self.registration_form,
            }
            return render(request, 'ADTAA/reg.html', context)

        new_user = self.registration_form.save()
        request.session['new_username'] = new_user.username

        return redirect('/ADTAA')


def logout(request):
    auth.logout(request)
    return render(request, 'ADTAA/logout.html')


class ChangePassword(View):
    form_class = ADTAA_forms.ChangePasswordForm

    def __init__(self):
        self.password_form = self.form_class()

    def get(self, request, *args, **kwargs):
        """
        This function checks to see if a valid user_object can be created from a request and returns a template
        rendered with a new PasswordForm if so
        :param request: Django Request object- request.SESSION['new_username'] must be a valid new username
        :param args: ~not used~
        :param kwargs: ~not used~
        :return: On Success: New PasswordForm rendered through a Django template
                 On Failure: redirect to 'not_found'
        """

        context = {
            'password_form': self.password_form,
        }
        return render(request, 'ADTAA/password.html', context)

    def post(self, request, *args, **kwargs):
        """
        This function checks to see if a valid user_object can be created from a request and then checks the POSTed
        form for validity. If the form is valid, the user's password is changed, the user is logged in, and is finally
        redirected to 'puzzles'
        :param request: Django Request object- request.SESSION['new_username'] must be a valid new username
        :param args: ~not used~
        :param kwargs: ~not used~
        :return: On Success: logged-in redirect to 'puzzles'
                 On Failure: Error PasswordForm rendered through a Django template or redirect to 'not_found' if valid
                 username not passed to function
        """

        self.password_form = self.form_class(request.POST)

        if not self.password_form.is_valid():
            context = {
                'password_form': self.password_form,
            }
            return render(request, 'ADTAA/password.html', context)

        self.password_form.save()
        return redirect('/ADTAA')

    @staticmethod
    def check_username(request):
        """
        This function checks that the session variable 'new_username' is set to a user that has an unusable password
        :param request: Django Request Object
        :return: On Success: the WordyUser instance where username=request.session['new_username']
                 On Failure: None
        """
        username = request.session.get('new_username', None)

        if not username:
            # TODO: Implement Django messaging service and then redirect to a site_error page that can consume
            # the messages passed to it. This will be much more useful than the simple not_found page that
            # has already been implemented.
            return None

        try:
            user_object = ADTAA_models.BaseUser.objects.get(
                username=username,
            )

            # The if/else statement below could be reduced to the following one-liner:
            # return user_object if not user_object.has_unusable_password() else None
            if user_object.has_usable_password():
                return None
            else:
                return user_object
        except ADTAA_models.BaseUser.DoesNotExist:
            # This exception isn't really an error. It just means that the username passed in does not exist in the
            # database. We don't need to stop the server for this issue, though we would probably want to log the
            # event in a production app.
            return None
        except Exception as e:
            raise_unexpected_error(e)


@login_required(login_url='/ADTAA/')
def user_page(request):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    context = {
        'user_type': user.user_type,
    }
    if request.method == 'POST':
        subject = 'ADTAA USER EXPERIENCE'
        body = request.POST['body']
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['tzolbayar58@gmail.com', ]
        send_mail(subject, body, email_from, recipient_list, fail_silently=False)
        messages.success(request, 'EMAIL HAS BEEN SENT SUCCESSFULLY.')
    return render(request, 'ADTAA/userPage.html', context)


def regRequests(request):
    queryset = ADTAA_models.BaseUser.objects.filter(isApproved="no")
    context = {
        'users': queryset
    }
    if request.method == 'POST':
        ADTAA_models.BaseUser.objects.update(isApproved="yes")
    return render(request, 'ADTAA/regRequests.html', context)
