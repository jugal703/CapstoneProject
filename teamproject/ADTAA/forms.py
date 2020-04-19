from django import forms
from django.forms import ValidationError
import datetime as dt
from ADTAA.globals import raise_unexpected_error
import ADTAA.models as base_models
import ADTAA.validators as validators

hours = [(None, 'Hour')] + [('{:02d}'.format(x), '{:02d}'.format(x)) for x in range(0, 24)]
mins = [(None, 'Minute')] + [('{:02d}'.format(i), '{:02d}'.format(i)) for i in range(60)]


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
        """
        This function creates and returns a new WordyUser instance from the Form data. The new WordyUser instance will
        have an unusable password
        :return: On Success: A new WordyUser instance with an unusable password
                 On Failure: Raises whichever error is caught
        """
        username = self.cleaned_data.get('email', None)
        password = self.cleaned_data.get('password', None)
        question1 = self.cleaned_data.get('question1', None)
        question2 = self.cleaned_data.get('question2', None)
        user_type = self.cleaned_data.get('user_type', None)

        try:
            new_user = base_models.BaseUser(
                username=username,
                sec_question1=question1,
                sec_question2=question2,
                user_type=user_type,
                isApproved="no",
            )
            new_user.set_password(password)
            new_user.save()

            return new_user
        except Exception as e:
            # We would never expect an error here because this function should only be called after checking to make
            # sure that the form is valid.
            raise_unexpected_error(e)


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

    def clean(self):
        """
        This function validates a Form instance by ensuring that the new password matches the verification password.
        Note that the first thing this function does is call its parent class's clean() function. That call will cause
        the wordy_validators.PasswordValidator() to run on this Form's instance of 'password' because a new instance
        of that class is passed to the form variable's 'validators' argument.
        :return: On Success: None
                 On Failure: Raises ValidationError
        """
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

    def save(self):
        """
        This function creates and returns a new WordyUser instance from the Form data. The new WordyUser instance will
        have an unusable password
        :return: On Success: A new WordyUser instance with an unusable password
                 On Failure: Raises whichever error is caught
        """
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
                user = base_models.BaseUser.objects.get(username=username)
                user.set_password(password)
                user.save()

            return user
        except Exception as e:
            # We would never expect an error here because this function should only be called after checking to make
            # sure that the form is valid.
            raise_unexpected_error(e)

        '''
        Please notice at this point that I have access to my user's new password IN PLAIN TEXT. You can verify
        that by printing out "password" or "verify_password" to the console. Those variables hold whatever our
        user entered in the HTML form. 

        I'm pointing this out in this long comment to highlight one of the many important reasons that you
        should be using some sort of password manager. You really need to be using unique passwords for every single
        website account that you use and it's just not feasible to keep up with that many unique and strong passwords.

        You really can't trust a website to not have access to the plaintext of any password you use for authentication
        unless you can read the source code for the site and somehow verify that the precise copy of the source code
        you read is the actual code running on both the server and client. Even then, Ken Thompson taught us that we
        can't trust any software stack that we haven't written ourselves. It's really best to just assume that any
        website you use has access to the plaintext version of the password you use for that site. That's why you
        need to be sure that you never reuse passwords.

        As developers, we're going to act ethically and verify our users' passwords using methods that won't allow us 
        to actually learn the password. We also won't store that plaintext password anywhere. However, it's a good idea 
        to assume that any website you visit was developed by unethical black hats that want to steal everything you 
        own.
        '''


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

    def save(self):
        """
        This function creates and returns a new WordyUser instance from the Form data. The new WordyUser instance will
        have an unusable password
        :return: On Success: A new WordyUser instance with an unusable password
                 On Failure: Raises whichever error is caught
        """
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

    def save(self):
        """
        This function creates and returns a new WordyUser instance from the Form data. The new WordyUser instance will
        have an unusable password
        :return: On Success: A new WordyUser instance with an unusable password
                 On Failure: Raises whichever error is caught
        """
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

            new_class.start_time = dt.datetime.strptime(hour + ':' + min + ':00', '%H:%M:%S').time()
            new_class.end_time = (dt.datetime.strptime(hour + ':' + min + ':00', '%H:%M:%S') + dt.timedelta(minutes=75)).time()
            new_class.save()

            return new_class
        except Exception as e:
            # We would never expect an error here because this function should only be called after checking to make
            # sure that the form is valid.
            raise_unexpected_error(e)


class NewInstructorForm(forms.ModelForm):
    class Meta:
        model = base_models.Instructor
        fields = ['instructor_id', 'last_name', 'maximum_class_load', 'disciplines_area']
        THE_CHOICES = base_models.DISCIPLINES_AREAS
        widgets = {
            'disciplines_area': forms.CheckboxSelectMultiple(choices=THE_CHOICES)
        }


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


class SolutionForm(forms.Form):
    courses = base_models.Class.objects.filter(assigned_instructor='No Instructor').all()
    instructors = forms.ModelChoiceField(queryset=base_models.Instructor.objects.all())




