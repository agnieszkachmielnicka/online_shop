from builtins import super

from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = ""
        self.fields['password'] = ""

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')


        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This is not correct user!")

            if not user.check_password(password):
                raise forms.ValidationError("This is not a correct password!")

            if not user.is_active:
                raise forms.ValidationError("This user is no longer active!")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Write your username'
        self.fields['email'].label = 'Write your email'
        self.fields['password1'].label = 'Give your password'
        self.fields['password2'].label = 'Confirm your password'
