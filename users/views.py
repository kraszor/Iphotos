from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegisterUserForm, EditProfileForm, FormChangePassword
from django.contrib.auth.decorators import login_required

from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseNotFound('Not Found')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in!")
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            else:
                return redirect('photo:home')
        else:
            messages.success(request, "Error! You've entered wrong username or password!")
            return redirect("users:login")

    else:
        return render(request, 'authenticate/login.html', {})


@login_required(login_url='users:login')
def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out!")
    return redirect("photo:home")


def register_user(request):
    if request.user.is_authenticated:
        return HttpResponseNotFound('Not Found')
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('authenticate/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, "Please confirm your email address to complete the registration")
            return redirect('users:login')
    else:
        form = RegisterUserForm()

    return render(request, 'authenticate/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect("users:login")
    else:
        messages.success(request, 'Activation link is invalid!')
        return redirect("users:login")


@login_required(login_url='users:login')
def profile(request):
    context = {'user': request.user}
    return render(request, 'authenticate/profile.html', context)


@login_required(login_url='users:login')
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been edited!")
            return redirect('users:profile')
        else:
            messages.success(request, "There was an error with your form!")
            return redirect('users:edit')

    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'authenticate/edit_profile.html', {'form': form})


@login_required(login_url='users:login')
def change_password(request):
    if request.method == "POST":
        form = FormChangePassword(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Successful password change!")
            return redirect('users:profile')
        else:
            messages.success(request, "There was an error!")
            return redirect('users:change_password')
    else:
        form = FormChangePassword(user=request.user)
        return render(request, 'authenticate/change_password.html', {'form': form})
