from django import forms
from django.forms import ValidationError, Select

from ADTAA.globals import raise_unexpected_error

import ADTAA.models as base_models
import ADTAA.validators as validators


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
        widget=forms.TextInput(attrs={'class': 'form_text_input', 'placeholder': 'Password'}),
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
                user_type=user_type
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
    )
    verify_password = forms.CharField(
        max_length=255,
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form_text_input', 'placeholder': 'Verify Password'})
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