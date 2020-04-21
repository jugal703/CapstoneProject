from django import forms
from django.forms import ValidationError
import datetime as dt
from ADTAA.globals import raise_unexpected_error
import ADTAA.models as base_models
import ADTAA.validators as validators

# formats to ensure that hours are 24-clock and 60 for minutes
hours = [(None, 'Hour')] + [('{:02d}'.format(x), '{:02d}'.format(x)) for x in range(0, 24)]
mins = [(None, 'Minute')] + [('{:02d}'.format(i), '{:02d}'.format(i)) for i in range(60)]

# form for user registration
# Allows public user of the application to select a requested user type,
# submit email address which will be the username of the user with a validator to validate email and that it is not an existing username,
# submit password of choice and validates that it is one that meets all the password rules
# submit answer to the two security questions
class RegistrationForm(forms.Form):
    user_type = forms.ChoiceField(
        label=False,
        widget=forms.Select,
        choices=[
            ('', 'Select a User Type'),
            ('admin', 'Admin'),
            ('scheduler', 'Scheduler'),
        ])

    email = forms.CharField(
        max_length=128,
        label=False,
        widget=forms.TextInput(attrs={'class': 'form_text_input', 'placeholder': 'Email'}),
        validators=[validators.NewUsernameValidator()],
    )
    password = forms.CharField(
        max_length=128,
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form_text_input', 'placeholder': 'Password'}),
        validators=[validators.PasswordValidator()],
    )
    question1 = forms.CharField(
        max_length=128,
        label=False,
        widget=forms.TextInput(
            attrs={'class': 'form_text_input', 'placeholder': 'What primary school did you attend?'}),
    )
    question2 = forms.CharField(
        max_length=128,
        label=False,
        widget=forms.TextInput(
            attrs={'class': 'form_text_input', 'placeholder': 'What is street did you live on as a child?'}),

    )

    def save(self):

        username = self.cleaned_data.get('email', None)
        password = self.cleaned_data.get('password', None)
        question1 = self.cleaned_data.get('question1', None)
        question2 = self.cleaned_data.get('question2', None)
        user_type = self.cleaned_data.get('user_type', None)

        # this function gets the inputted values and creates a new user in our BaseUser model
        # important to note that isApproved is set to 'no' as it will require root user to be switched to 'yes'
        try:
            new_user = base_models.BaseUser(
                username=username,
                sec_question1=question1,
                sec_question2=question2,
                user_type=user_type,
                isApproved="no",
            )
            new_user.set_password(password)  # set the chosen password as the password for that requested user
            new_user.save()  # save the new user to the database

            return new_user
        except Exception as e:
            # We would never expect an error here because this function should only be called after checking to make
            # sure that the form is valid.
            raise_unexpected_error(e)

# form to allow all registered users to change their chosen password
# requires registered user to submit their email (username) for the app
# requires registered user to answer the security questions with their preset answers
# requires registered user to submit a new password and validates to check that the new password meets our password rules
# requires registered user to submit a password verification
class ChangePasswordForm(forms.Form):
    email = forms.CharField(
        max_length=128,
        label=False,
        widget=forms.TextInput(attrs={'class': 'form_text_input', 'placeholder': 'Email'}),
        validators=[validators.PassWordUsernameValidator()],

    )
    question1 = forms.CharField(
        max_length=128,
        label=False,
        widget=forms.TextInput(
            attrs={'class': 'form_text_input', 'placeholder': 'What primary school did you attend?'}),
    )
    question2 = forms.CharField(
        max_length=128,
        label=False,
        widget=forms.TextInput(
            attrs={'class': 'form_text_input', 'placeholder': 'What is street did you live on as a child?'}),
    )
    new_password = forms.CharField(
        max_length=255,
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form_text_input', 'placeholder': 'New Password'}),
        validators=[validators.PasswordValidator()],
    )
    verify_password = forms.CharField(
        max_length=255,
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form_text_input', 'placeholder': 'Verify Password'}),
    )
    # function to get the values submitted for new password and password verification to ensure that it is the same
    # throws a validation error if the two password entries are different
    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data.get('new_password', None)
        verify_password = cleaned_data.get('verify_password', None)

        if not password or not verify_password:
            raise ValidationError(
                'Invalid Password',
                code='invalid',
            )

        if not password == verify_password:
            raise ValidationError(
                'Passwords did not match',
                code='invalid',
            )

    # function gets all the data entered and filters through the BaseUser model to find a match with the registered
    # user's entry of username, answer to security question1, and answer to security question2
    def save(self):

        username = self.cleaned_data.get('email', None)
        question1 = self.cleaned_data.get('question1', None)
        question2 = self.cleaned_data.get('question2', None)
        password = self.cleaned_data.get('new_password', None)

        try:
            user = base_models.BaseUser.objects.all().filter(
                username=username,
                sec_question1=question1,
                sec_question2=question2
            ).count()
            if user:
                # if a match is found in the database then it gets the user's username and sets the entered new password
                # as the password for that user and saves it
                user = base_models.BaseUser.objects.get(username=username)
                user.set_password(password)
                user.save()
            return user
        except Exception as e:
            # We would never expect an error here because this function should only be called after checking to make
            # sure that the form is valid.
            raise_unexpected_error(e)

# form to add new instructor to Instructors Model
# requires ID and last name of the instructor
# requires maximum load per semester for the instructor with choice from 1 to 4
# requires discipline areas of the instructor based off the list of discipline areas set
class InstructorForm(forms.Form):
    instructor_id = forms.CharField(
        max_length=128,
        label=False,
        widget=forms.TextInput(attrs={'class': 'form_text_input', 'placeholder': 'Instructor ID'}),
    )
    last_name = forms.CharField(
        max_length=128,
        label=False,
        widget=forms.TextInput(attrs={'class': 'form_text_input', 'placeholder': 'Instructor Last Name'}),
    )
    maximum_class_load = forms.ChoiceField(
        label=False,
        widget=forms.Select,
        choices=[
            ('', 'Select Maximum Class Load Per Semester'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
        ]
    )
    discipline_areas = forms.MultipleChoiceField(
        label="Discipline Areas",
        widget=forms.CheckboxSelectMultiple,
        choices=base_models.DISCIPLINES_AREAS
    )

    # function to save the added instructor with its entries to the database
    def save(self):
        instructor_id = self.cleaned_data.get('instructor_id', None)
        last_name = self.cleaned_data.get('last_name', None)
        maximum_class_load = self.cleaned_data.get('maximum_class_load', None)
        discipline_areas = self.cleaned_data.get('discipline_areas', None)

        try:
            new_instructor = base_models.Instructor(
                instructor_id=instructor_id,
                last_name=last_name,
                maximum_class_load=maximum_class_load,

            )
            new_instructor.save()

            for i in discipline_areas:
                discipline_area = base_models.DisciplinesAreas.objects.get(disciplines_area=i)
                new_instructor.disciplines_area.add(discipline_area)
            new_instructor.save()

            return new_instructor
        except Exception as e:
            # We would never expect an error here because this function should only be called after checking to make
            # sure that the form is valid.
            raise_unexpected_error(e)

# form to add new class to Class Model
# requires course number and title of the instructor
# requires meetings days for the class with choice of 'Monday and Wednesday' or 'Tuesday and Thursday'
# requires the starting hour and minute of the class on a 24-hr clock format,
# ending time is calculating as 75-mins after the start time
# requires discipline areas of the class based off the list of discipline areas set
class ClassForm(forms.Form):
    course_number = forms.CharField(
        max_length=128,
        label=False,
        widget=forms.TextInput(attrs={'class': 'form_text_input', 'placeholder': 'Course Number'}),
    )
    course_title = forms.CharField(
        max_length=128,
        label=False,
        widget=forms.TextInput(attrs={'class': 'form_text_input', 'placeholder': 'Course Title'}),
    )
    meeting_days = forms.ChoiceField(
        label=False,
        widget=forms.Select,
        choices=[
            ('', 'Select Meeting Days'),
            ('MW', 'Monday and Wednesday'),
            ('TR', 'Tuesday and Thursday'),
        ]
    )
    hour = forms.ChoiceField(
        label="Start Hour and Minute (75 min class)",
        widget=forms.Select,
        choices=hours
    )

    min = forms.ChoiceField(
        label=False,
        widget=forms.Select,
        choices=mins
    )
    discipline_areas = forms.MultipleChoiceField(
        label="Discipline Areas",
        widget=forms.CheckboxSelectMultiple,
        choices=base_models.DISCIPLINES_AREAS
    )

    # function to save the added instructor with its entries to the database
    def save(self):
        course_number = self.cleaned_data.get('course_number', None)
        course_title = self.cleaned_data.get('course_title', None)
        meeting_days = self.cleaned_data.get('meeting_days', None)
        hour = self.cleaned_data.get('hour', None)
        min = self.cleaned_data.get('min', None)
        discipline_areas = self.cleaned_data.get('discipline_areas', None)

        try:
            new_class = base_models.Class(
                course_number=course_number,
                course_title=course_title,
                meeting_days=meeting_days,
            )
            new_class.save()

            for i in discipline_areas:
                discipline_area = base_models.DisciplinesAreas.objects.get(disciplines_area=i)
                new_class.disciplines_area.add(discipline_area)
            # calculates the end time of the class to be 75 minutes after the start time
            new_class.start_time = dt.datetime.strptime(hour + ':' + min + ':00', '%H:%M:%S').time()
            new_class.end_time = (
                    dt.datetime.strptime(hour + ':' + min + ':00', '%H:%M:%S') + dt.timedelta(minutes=75)).time()
            new_class.save()

            return new_class
        except Exception as e:
            # We would never expect an error here because this function should only be called after checking to make
            # sure that the form is valid.
            raise_unexpected_error(e)

# form to edit a instructor already in the Instructor model database
class NewInstructorForm(forms.ModelForm):
    class Meta:
        model = base_models.Instructor
        fields = ['instructor_id', 'last_name', 'maximum_class_load', 'disciplines_area']
        THE_CHOICES = base_models.DISCIPLINES_AREAS
        widgets = {
            'disciplines_area': forms.CheckboxSelectMultiple(choices=THE_CHOICES)
        }

# form to edit a class already in the Class model database
class NewClassForm(forms.ModelForm):
    class Meta:
        model = base_models.Class
        fields = ['course_number', 'course_title', 'meeting_days', 'start_time', 'end_time', 'disciplines_area']
        THE_CHOICES = base_models.DISCIPLINES_AREAS
        widgets = {
            'disciplines_area': forms.CheckboxSelectMultiple(choices=THE_CHOICES),
        }
        labels = {
            'start_time': "Start Time (hh:mm:ss 24-hour clock)",
            'end_time': "End Time (75 min after start time)"
        }

# form to edit solution by pulling all the courses and allowing the user to select which instructor is assigned to it
class SolutionForm(forms.Form):
    courses = base_models.Class.objects.all()
    instructors = forms.ModelChoiceField(queryset=base_models.Instructor.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.courses = base_models.Class.objects.all()
    # function to save the assigned instructors to the 'assigned_instructor' field in Class model
    def save(self, class_num):
        instructor = self.cleaned_data.get('instructors', None)
        if instructor:
            c = self.courses[class_num]
            c.assigned_instructor = str(instructor)
            c.save()
