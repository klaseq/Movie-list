from django import forms
from .models import Movie, User, Tag

class MovieForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset = Tag.objects.all(), required = False)
    class Meta:
        model = Movie
        fields = ["name", "director", "genre", "tags"]

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ["email", "password"]

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = ["email", "password"]

