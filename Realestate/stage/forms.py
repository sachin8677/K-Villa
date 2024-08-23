from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, BuyerProfile, SellerProfile, Property

class BuyerSignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_buyer = True
        if commit:
            user.save()
            BuyerProfile.objects.create(user=user, phone_number=self.cleaned_data.get('phone_number'))
        return user

class SellerSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=15)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'company_name', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.save()
            SellerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data.get('company_name'),
                phone_number=self.cleaned_data.get('phone_number')
            )
        return user

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'image','location']