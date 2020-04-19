import random
from django.contrib import auth
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils.decorators import method_decorator


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
                'error': 'Must Pass In Every Verification.'
            }
            return render(request, 'ADTAA/index.html', context=context)

        try:
            user = ADTAA_models.BaseUser.objects.get(username=email)
        except ADTAA_models.BaseUser.DoesNotExist:
            context = {
                'error': 'User Does Not Exist.'
            }
            return render(request, 'ADTAA/index.html', context=context)

        if user.check_password(password):
            if user.isApproved == "yes":
                if user.user_type == "root":
                    login(request, user)
                    request.session['username'] = email
                    return redirect('/ADTAA/rootHome', request)
                if user.user_type == "admin":
                    login(request, user)
                    request.session['username'] = email
                    return redirect('/ADTAA/adminHome', request)
                if user.user_type == "scheduler":
                    login(request, user)
                    request.session['username'] = email
                    return redirect('/ADTAA/schedulerHome', request)
            else:
                context = {
                    'error': 'User Has Not Been Approved Yet'
                }
                subject = 'ADTAA UNAPPROVED USER LOGIN'
                body = email + ' is attempting to login but has not been approved yet. Please approve or deny this user ASAP. - MindDebuggers'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['txzolbayar@ualr.edu', ]
                send_mail(subject, body, email_from, recipient_list, fail_silently=False)
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
    instructors_list = ADTAA_models.Instructor.objects.all
    classes_list = ADTAA_models.Class.objects.all

    context = {
        'instructors': instructors_list,
        'classes': classes_list,
    }

    if request.method == 'POST':
        if 'instrDelete' in request.POST:
            instructor_id = request.POST.get("instrDelete", "")
            instructor = ADTAA_models.Instructor.objects.get(instructor_id=instructor_id)
            instructor.delete()
        elif 'classDelete' in request.POST:
            course_number = request.POST.get("classDelete", "")
            course = ADTAA_models.Class.objects.get(course_number=course_number)
            course.delete()

    return render(request, 'ADTAA/rootHome.html', context)


@login_required
@admin_required
def admin_home_page(request):
    instructors_list = ADTAA_models.Instructor.objects.all
    classes_list = ADTAA_models.Class.objects.all

    context = {
        'instructors': instructors_list,
        'classes': classes_list,
    }

    if request.method == 'POST':
        if 'instrDelete' in request.POST:
            instructor_id = request.POST.get("instrDelete", "")
            instructor = ADTAA_models.Instructor.objects.get(instructor_id=instructor_id)
            instructor.delete()
        elif 'classDelete' in request.POST:
            course_number = request.POST.get("classDelete", "")
            course = ADTAA_models.Class.objects.get(course_number=course_number)
            course.delete()

    return render(request, 'ADTAA/adminHome.html', context)


@login_required
@scheduler_required
def scheduler_home_page(request):
    instructors_list = ADTAA_models.Instructor.objects.all
    classes_list = ADTAA_models.Class.objects.all

    context = {
        'instructors': instructors_list,
        'classes': classes_list,
    }
    return render(request, 'ADTAA/schedulerHome.html', context)


@login_required
@admin_root_required
def setup_instructor(request):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    context = {
        'user_type': user.user_type
    }
    return render(request, 'ADTAA/instrSetup.html', context)


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
    form = ADTAA_forms.SolutionForm
    context = {
        'user_type': user.user_type,
        'form': form
    }

    if request.method == 'POST':
        form = ADTAA_forms.SolutionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solution Has Been Saved.')
    return render(request, 'ADTAA/editSolutions.html', context)


def make_solution(classes, instructors_load, rest_classes, curr_solution):
    for i, elem in enumerate(classes):
        if len(instructors_load) == 0:
            break
        if len(rest_classes) == 0:
            break
        curr_class = ADTAA_models.Class.objects.get(course_number=classes[i][0])
        class_start_time = curr_class.start_time
        class_end_time = curr_class.end_time
        class_day = curr_class.meeting_days

        for instructor in classes[i][1]:
            if instructor not in instructors_load:
                continue
            else:
                curr_instructor_classes = curr_solution[instructor]
                time_conflict = False
                for c in curr_instructor_classes:
                    instructor_class = ADTAA_models.Class.objects.get(course_number=c)
                    c_start_time = instructor_class.start_time
                    c_end_time = instructor_class.end_time
                    c_day = instructor_class.meeting_days
                    if class_day == c_day and (class_end_time > c_start_time or class_start_time < c_end_time):
                        time_conflict = True
                        break
                if time_conflict:
                    continue
                else:
                    instructors_load[instructor] = instructors_load[instructor] - 1
                    curr_solution[instructor].append(classes[i][0])

                    del rest_classes[classes[i][0]]
                    if instructors_load[instructor] == 0:
                        del instructors_load[instructor]
                        if len(instructors_load) == 0:
                            break
                    if len(rest_classes) == 0:
                        break
                    break
    return len(rest_classes)


@method_decorator(login_required(), name='get')
class GenerateSolutions(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get('username', '0')
        user = ADTAA_models.BaseUser.objects.get(username=username)

        context = {
            'user_type': user.user_type,
        }
        return render(request, 'ADTAA/generateSolutions.html', context)

    def post(self, request, *args, **kwargs):
        if 'create_solution' in request.POST:
            username = request.session.get('username', '0')
            user = ADTAA_models.BaseUser.objects.get(username=username)
            instructors_list = ADTAA_models.Instructor.objects.all()
            classes_list = ADTAA_models.Class.objects.all()
            classes = {}
            not_assigned_classes = []
            instructors_load = {}
            temp_solution = {}
            i_list = []

            for i in instructors_list:
                i_list.append(i.instructor_id)
                instructors_load[i.instructor_id] = int(i.maximum_class_load)
                temp_solution[i.instructor_id] = []

            biggest_disciplines_area_count = 0
            for i in classes_list:
                classes[i.course_number] = [i.disciplines_area.count()]
                for j in instructors_list:
                    if any(x in list(i.disciplines_area.all()) for x in list(j.disciplines_area.all())):
                        if j.disciplines_area.count() > biggest_disciplines_area_count:
                            classes[i.course_number].insert(1, j.instructor_id)
                            biggest_disciplines_area_count = j.disciplines_area.count()
                        else:
                            classes[i.course_number].append(j.instructor_id)
                    else:
                        if j == instructors_list.last() and len(classes[i.course_number]) == 1:
                            not_assigned_classes.append(i.course_number)
                            del classes[i.course_number]

            # one_instructor_classes = {k: v for k, v in classes.items() if len(v) == 2}
            # classes = {k: v for k, v in classes.items() if len(v) > 2}

            # sort classes by disciplines_area numbers
            classes = {k: v for k, v in sorted(classes.items(), key=lambda item: item[1], reverse=True)}
            classes = list(classes.items())
            for c in classes:
                c[1].pop(0)
            rest_classes = dict(classes)
            print("before solution:", classes)
            # print("one_instructor_classes:", one_instructor_classes)
            print("not_assigned_classes", not_assigned_classes)

            classes = classes.copy()
            temp_instructors_load = instructors_load.copy()
            not_assigned_classes_num = make_solution(classes, temp_instructors_load, rest_classes,
                                                     temp_solution)

            print(rest_classes)
            print(temp_solution)

            if len(rest_classes) == 0:
                best_solution = temp_solution.copy()
                lowest_not_assigned_classes = rest_classes
            else:
                best_solution = temp_solution.copy()
                lowest_not_assigned_classes = rest_classes
                for x in range(0, 50):
                    temp_classes = random.sample(classes, len(classes))
                    for i in temp_classes:
                        random.shuffle(i[1])
                    temp_instructors_load = instructors_load.copy()
                    rest_classes = dict(temp_classes)
                    for i in instructors_list:
                        temp_solution[i.instructor_id] = []
                    print('-----------')
                    print(temp_classes)
                    new_not_assigned_classes_num = make_solution(temp_classes, temp_instructors_load, rest_classes,
                                                                 temp_solution)
                    print(temp_solution)
                    print(rest_classes)
                    if new_not_assigned_classes_num < not_assigned_classes_num:
                        not_assigned_classes_num = new_not_assigned_classes_num
                        lowest_not_assigned_classes = rest_classes
                        best_solution = temp_solution.copy()
                        print("!")
                    if len(rest_classes) == 0:
                        break

            solution_context = []
            for instructor, classes in best_solution.items():
                i = ADTAA_models.Instructor.objects.get(instructor_id=instructor)
                for c in classes:
                    instructor_class = ADTAA_models.Class.objects.get(course_number=c)
                    solution_context.append({'Course_number': instructor_class.course_number,
                                             'Course_title': instructor_class.course_title,
                                             'Start_time': instructor_class.start_time,
                                             'Meeting_days': instructor_class.meeting_days,
                                             'End_time': instructor_class.end_time,
                                             'Instructor': i.last_name,
                                             'Instructor_id': i.instructor_id})
            print(solution_context)

            for i in not_assigned_classes:
                lowest_not_assigned_classes[i] = ''
            not_assigned_classes_context = []
            for c in lowest_not_assigned_classes:
                not_assigned_class = ADTAA_models.Class.objects.get(course_number=c)
                not_assigned_classes_context.append({'Course_number': not_assigned_class.course_number,
                                                     'Course_title': not_assigned_class.course_title,
                                                     'Meeting_days': not_assigned_class.meeting_days,
                                                     'Start_time': not_assigned_class.start_time,
                                                     'End_time': not_assigned_class.end_time,
                                                     })
            request.session['solution'] = best_solution
            context = {
                'solution': solution_context,
                'no_assigned_class': not_assigned_classes_context,
                'user_type': user.user_type
            }
            return render(request, 'ADTAA/generateSolutions1.html', context)

        if 'print' in request.POST:
            username = request.session.get('username', '0')
            user = ADTAA_models.BaseUser.objects.get(username=username)
            context = {
                'save': "Solution Printed!",
                'user_type': user.user_type
            }
            return render(request, 'ADTAA/generateSolutions.html', context)

        if 'save' in request.POST:
            username = request.session.get('username', '0')
            user = ADTAA_models.BaseUser.objects.get(username=username)
            best_solution = request.session.get('solution', None)
            if best_solution:
                for instructor, classes in best_solution.items():
                    instructor = ADTAA_models.Instructor.objects.get(instructor_id=instructor)
                    for c in classes:
                        instructor_class = ADTAA_models.Class.objects.get(course_number=c)
                        instructor_class.assigned_instructor = instructor.instructor_id
                        instructor_class.save()

            context = {
                'save': "Solution Saved!",
                'user_type': user.user_type
            }
            return render(request, 'ADTAA/generateSolutions.html', context)

        if 'reset' in request.POST:
            username = request.session.get('username', '0')
            user = ADTAA_models.BaseUser.objects.get(username=username)
            classes_list = ADTAA_models.Class.objects.all()
            for c in classes_list:
                c.assigned_instructor = "No Instructor"
                c.save()

            context = {
                'save': "Solution Reset!",
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
        subject = 'ADTAA NEW USER REGISTRATION'
        body = 'A new user has registered to be a user of ADTAA. - MindDebuggers'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['txzolbayar@ualr.edu', ]
        send_mail(subject, body, email_from, recipient_list, fail_silently=False)
        messages.success(request, 'Thank you for registering. You registration request is awaiting approval.')

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
        messages.success(request, 'Your Password Has Been Changed.')
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


@login_required
@root_required
def regRequests(request):
    queryset = ADTAA_models.BaseUser.objects.filter(isApproved="no")

    context = {
        'users': queryset
    }

    if request.method == 'POST':
        if 'Approve' in request.POST:
            username = request.POST.get("Approve", "")
            user = ADTAA_models.BaseUser.objects.get(username=username)
            user.isApproved = "yes"
            user.save()
            subject = 'ADTAA USER LOGIN'
            body = 'Congratulations! You have been approved to be a user of ADTAA! Please login with the credentials you have set. - MindDebuggers'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [username, ]
            send_mail(subject, body, email_from, recipient_list, fail_silently=False)

        elif 'Deny' in request.POST:
            username = request.POST.get("Deny", "")
            user = ADTAA_models.BaseUser.objects.get(username=username)
            user.delete()
            subject = 'ADTAA USER LOGIN'
            body = 'We thank you for your registration to be a user of ADTAA. However, you have been denied the ability to be a user of ADTAA. - MindDebuggers'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [username, ]
            send_mail(subject, body, email_from, recipient_list, fail_silently=False)

    return render(request, 'ADTAA/regRequests.html', context)


@method_decorator(admin_root_required, name='get')
class AddClass(View):
    form_class = ADTAA_forms.ClassForm

    def __init__(self):
        self.class_form = self.form_class()

    def get(self, request, *args, **kwargs):
        username = self.request.session.get('username', '0')
        user = ADTAA_models.BaseUser.objects.get(username=username)
        context = {
            'class_form': self.class_form,
            'user_type': user.user_type,
        }
        return render(request, 'ADTAA/classSetup.html', context)

    def post(self, request, *args, **kwargs):
        self.class_form = self.form_class(request.POST)
        if not self.class_form.is_valid():
            context = {
                'class_form': self.class_form,
            }
            return render(request, 'ADTAA/classSetup.html', context)

        self.class_form.save()
        messages.success(request, 'Class Has Been Successfully Added.')

        return redirect('/ADTAA/classSetup')


@method_decorator(admin_root_required, name='get')
class AddInstructor(View):
    form_instructor = ADTAA_forms.InstructorForm

    def __init__(self):
        self.instructor_form = self.form_instructor()

    def get(self, request, *args, **kwargs):
        username = self.request.session.get('username', '0')
        user = ADTAA_models.BaseUser.objects.get(username=username)
        context = {
            'instructor_form': self.instructor_form,
            'user_type': user.user_type,
        }
        return render(request, 'ADTAA/instrSetup.html', context)

    def post(self, request, *args, **kwargs):
        self.instructor_form = self.form_instructor(request.POST)
        if not self.instructor_form.is_valid():
            context = {
                'class_form': self.instructor_form,
            }
            return render(request, 'ADTAA/instrSetup.html', context)

        self.instructor_form.save()
        messages.success(request, 'Instructor Has Been Successfully Added.')

        return redirect('/ADTAA/instrSetup')


@login_required
@admin_root_required
def edit_instructor(request, pk):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    instructor = ADTAA_models.Instructor.objects.get(id=pk)

    form = ADTAA_forms.NewInstructorForm(instance=instructor)

    context = {
        'user_type': user.user_type,
        'form': form
    }
    if request.method == 'POST':
        form = ADTAA_forms.NewInstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes Have Been Successfully Made.')

    return render(request, 'ADTAA/editInstr.html', context)


@login_required
@admin_root_required
def edit_class(request, pk):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    course = ADTAA_models.Class.objects.get(id=pk)

    form = ADTAA_forms.NewClassForm(instance=course)

    context = {
        'user_type': user.user_type,
        'form': form
    }
    if request.method == 'POST':
        form = ADTAA_forms.NewClassForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes Have Been Successfully Made.')

    return render(request, 'ADTAA/editClass.html', context)


@login_required
def instructor_profile(request, pk):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    instructor = ADTAA_models.Instructor.objects.get(id=pk)

    context = {
        'user_type': user.user_type,
        'instructor': instructor,
    }
    if request.method == 'POST':
        if 'instrDelete' in request.POST:
            instructor = ADTAA_models.Instructor.objects.get(instructor_id=instructor)
            instructor.delete()
            messages.success(request, 'Instructor Has Been Deleted.')
    return render(request, 'ADTAA/instructorProfile.html', context)


@login_required
def class_profile(request, pk):
    username = request.session.get('username', '0')
    user = ADTAA_models.BaseUser.objects.get(username=username)
    course = ADTAA_models.Class.objects.get(id=pk)

    context = {
        'user_type': user.user_type,
        'course': course,
    }
    if request.method == 'POST':
        if 'classDelete' in request.POST:
            course = ADTAA_models.Class.objects.get(course_number=course)
            course.delete()
            messages.success(request, 'Class Has Been Deleted.')
    return render(request, 'ADTAA/classProfile.html', context)
