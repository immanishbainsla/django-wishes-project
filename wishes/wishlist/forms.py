from django import forms

from wishlist.models import UserWishListModel, ContactModel

# from django.contrib.auth import get_user_model

from django.contrib.auth.models import User

from django.urls import reverse
from django.contrib.auth import authenticate

# FORMS goes here.
class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class UserLogInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password')

    def clean(self):
        all_clean_data = super().clean()
        username = all_clean_data['username']
        password = all_clean_data['password']

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("USERNAME or PASSWORD is INCORRECT!")
        else:
            return reverse('index')


class UserWishListForm(forms.ModelForm):

    class Meta():
        model = UserWishListModel
        fields = ('title', 'description',)


# <!-- {{ form|crispy }} -->
# <!-- {{ form.name|as_crispy_field }} -->

class UserContactForm(forms.ModelForm):

    class Meta():
        model = ContactModel
        fields = ('name', 'email', 'query')
