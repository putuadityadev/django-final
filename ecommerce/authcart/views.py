from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login, logout

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('pass1', '')
        confirm_password = request.POST.get('pass2', '')
        
        # Validasi email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format!')
            return render(request, 'authentication/signup.html')
        
        # Validasi password
        if password != confirm_password:
            messages.warning(request, 'Passwords do not match!')
            return render(request, 'authentication/signup.html')
        
        try:
            # Cek email sudah digunakan
            if User.objects.filter(username=email).exists():
                messages.info(request, 'Email already in use!')
                return render(request, 'authentication/signup.html')
            
            # Buat user
            user = User.objects.create_user(
                username=email, 
                email=email, 
                password=password
            )
            user.is_active = False
            user.save()

            # Persiapan email aktivasi
            email_subject = "Activate Your Account"
            message = render_to_string('authentication/activate.html', {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })

            try:
                # Kirim email aktivasi
                email_message = EmailMessage(
                    email_subject, 
                    message, 
                    settings.EMAIL_HOST_USER, 
                    [email]
                )
                email_message.content_subtype = 'html'
                email_message.send()
                
                # Pesan sukses
                messages.success(request, 'Check your email to activate your account.')
                return redirect('/auth/login/')
            
            except Exception as email_error:
                # Hapus user jika email gagal dikirim
                user.delete()
                messages.error(request, f'Failed to send activation email: {email_error}')
                return render(request, 'authentication/signup.html')
        
        except Exception as e:
            # Tangani error umum
            messages.error(request, f'Signup failed: {str(e)}')
    
    return render(request, 'authentication/signup.html')

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            # Dekode user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Validasi user dan token
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Account Activated Successfully')
            return redirect('/auth/login/')
        
        # Jika aktivasi gagal
        messages.error(request, 'Activation link is invalid!')
        return render(request, 'auth/activatefail.html')

def handle_login(request):
    if request.method == 'POST':
        username = request.POST['email']
        userpassword = request.POST['pass1']
        myuser = authenticate(username=username, password=userpassword)
        
        if myuser is not None:
            login(request, myuser)
            messages.success(request, 'Login Success')
            return redirect('/')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'authentication/login.html')

    return render(request, 'authentication/login.html')


def handle_logout(request):
    logout(request)
    messages.warning(request, 'Logout Success')
    return redirect('/auth/login')