from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'password', 'text']
