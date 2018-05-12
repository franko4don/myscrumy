from django import forms
from django.core.exceptions import ValidationError
import json
from nwanzescrumy.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

# class UserForm(forms.Form):
#     first_name = forms.CharField(label='First name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
#     last_name = forms.CharField(label='Last name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
#     username = forms.CharField(label='User name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
#     email = forms.EmailField(label='Email', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
#     password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control'}))

#     class Meta:
#         model = ScrumyUser
#         fields = ['first_name', 'last_name', 'username', 'email', 'password']

#     def clean_email(self):
#         data = self.cleaned_data['email']
        
#         if ScrumyUser.objects.filter(email=data).count() > 0:
#             raise ValidationError(_('Email Already Exists'))
#         return data
    
#     def clean_username(self):
#         data = self.cleaned_data['username']
        
#         if ScrumyUser.objects.filter(username=data).count() > 0:
#             raise ValidationError(_('user name Already Exists'))
#         return data


class GoalForm(forms.Form):
    stata = [(obj.id, obj.status) for obj in GoalStatus.objects.all()]
    CHOICES= (
            stata
        )
    goal_description = forms.CharField(widget=forms.Textarea(attrs={'rows': "6",'class':'form-control' }))
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=CHOICES)

    class Meta:
        model = Task
        fields = ['goal_description']
     
    def clean_description(self):
        data = self.cleaned_data['goal_description']
        
        if len(data.strip()) < 10:
            raise ValidationError(_('Goal Description is short'))
        return data


class ChangeGoalStatusForm(forms.Form):
    status = [(obj.id, obj.status) for obj in GoalStatus.objects.all()]
    CHOICES= (
            status
        )
    USERS =(
        [(obj.id, obj.username) for obj in User.objects.all()]
    )
    goal_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=CHOICES)
    assigned_to = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=USERS)
    class Meta:
        model = ScrumyGoal
        fields = ['goal_description', 'status']
    
