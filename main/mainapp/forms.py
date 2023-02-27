from django import forms

class UserInputForm(forms.Form):
    store_item = forms.CharField(max_length=100)