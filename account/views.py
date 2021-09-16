from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from django.http import HttpResponse
from django.template.loader import render_to_string

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import AccountActivationTokenGenerator
from .forms import RegistrationForm
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
            account_activation_token = AccountActivationTokenGenerator()
            message = render_to_string('account/registration/account_activation_email.html  ', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject=subject, message=message)
            print("returning http response")
            return HttpResponse("Registered successfully and sent the token")
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
    except Exception as activate_ex:
        print("User activation failed with {0}".format(activate_ex))
    account_activation_token = AccountActivationTokenGenerator()
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        redirect('account:dashboard')
    else:
        return  render(request, 'account/registration/activation_invalid.html')


@login_required
def dashboard(request):
    #orders = user_orders(request)
    # context = {
    #     'section':profile,
    #     'orders':orders,
    # }
    return render(request, 'account/user/dashboard.html' )