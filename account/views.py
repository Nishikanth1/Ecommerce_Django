from django.shortcuts import render

# Create your views here.
from .forms import RegistrationForm

def account_register(request):
    # if request.user.is_authenticated:
    #     return redirect('/')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=True)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = 'False'
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string('account/registration/account_activation_email.html  ', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject=subject, message=message)
    else:
        print("in else form")
        registerForm = RegistrationForm()
        context = {
            'form': registerForm
        }
        return render(request, 'account/registration/register.html',context=context)
