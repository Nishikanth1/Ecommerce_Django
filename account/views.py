from django.shortcuts import render

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistrationForm, UserEditForm
from .models import  UserBase
from .tokens import account_activation_token
# Create your views here.
def account_register(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    print("in account register")
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            print("register account form is valid")
            user = registerForm.save(commit=True)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = 'False'
            user.save()
            current_site = get_current_site(request)
            print("user save in account register")
            subject = "Activate your Account"
            #account_activation_token = AccountActivationTokenGenerator()
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject=subject, message=message)
            print("returning http response")
            return HttpResponse("Registered successfully and sent the token")
        else:
            print("form erroes {0}".format(registerForm.errors))
            return HttpResponse("Invalid details entered")
    else:
        print("in else form")
        registerForm = RegistrationForm()
        context = {
            'form': registerForm
        }
        return render(request, 'account/registration/register.html',context=context)

def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
        print("user {0}".format(user))
        print("token {0}".format(token))
        #account_activation_token = AccountActivationTokenGenerator()
        token_correct = account_activation_token.check_token(user, token)
        print("token correct = {0}".format(token_correct))
        if user is not None and token_correct:
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('account:dashboard')
        else:
            return render(request, 'account/registration/activation_invalid.html')
    except Exception as activate_ex:
        print("User activation failed with {0}".format(activate_ex))

@login_required
def dashboard(request):
    #orders = user_orders(request)
    # context = {
    #     'section':profile,
    #     'orders':orders,
    # }
    return render(request, 'account/user/dashboard.html' )

@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            print("valid form")
            user_form.save()
        else:
            print("erros {0}".format(user_form.errors))
            print("invalid form")
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'user_form': user_form
    }
    return render(request, 'account/user/edit_details.html', context)

@login_required
def delete_user(request):
    print("getting user to be deleted")
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    print("user set to inactive")
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')