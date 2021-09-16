from django import  forms
from .models import UserBase

class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Enter Username ',min_length=4, max_length=150,help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required':'Sorry, you need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email')

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count:
            print("error clean username")
            raise forms.ValidationError("Username already exists")
        print("end clean username")
        return user_name

    def clean_password2(self):
        c_d = self.cleaned_data
        if c_d['password'] != c_d['password2']:
            print("password1 {0}".format(c_d['password']))
            print("password2 {0}".format(c_d['password2']))
            print("dir c_D {0}".format(dir(c_d)))
            print("error clean password2")
            raise forms.ValidationError('Passwords do not match')
        print("end clean password2")
        return c_d['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            print("emails is {0}".format(email))
            print("email errprs {0}".format(dir(email)))
            print("error clean email")
            raise forms.ValidationError("Email Already exists, please login")

        print("end clean email")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'} )
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Email' , 'name':'email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'}
        )

