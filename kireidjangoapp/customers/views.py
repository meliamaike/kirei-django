from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm, IngresarForm
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from customers.models import Customer
from django.db.models.query_utils import Q


def register(request):
    user = request.user
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, "Se ha registrado exitosamente.")
            return redirect("/")
        messages.error(request, "Error.")
    form = RegisterForm()
    return render(
        request=request, template_name="customers/register.html", context={"register_form": form}
    )


def login(request):
    if request.method == 'POST':
        form = IngresarForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                remember_me = request.POST.get('remember', False)
                if remember_me:
                    request.session.set_expiry(30 * 24 * 60 * 60) # 30 days
                else:
                    request.session.set_expiry(0) # Session ends when the user closes their browser
                return redirect('home')
            else:
                form.add_error(None, 'Invalid Login Credentials')
    else:
        form = IngresarForm()

    form.helper = FormHelper()
    form.helper.form_method = 'post'
    form.helper.layout = Layout(
        Field('login', placeholder='', autofocus="", label="Email"),
        Field('password', placeholder='', label="Contraseña"),
        Field('remember', label="Recuérdame"),
    )

    context = {'login_form': form}
    return render(request, 'customers/login.html', context)


# Cerrar sesion
def logout(request):
    logout(request)
    messages.info(request, "Ha cerrado sesión correctamente.")
    return redirect("home:index")

# Olvido de contraseña
def password_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = Customer.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Cambio de contraseña"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "Kirei estética",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "hola@kirei.com",
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Se encontró una cabecera invalida..")
                    # return redirect("/password_reset/done/")
                    messages.success(
                        request,
                        "Te enviamos un e-mail con las instrucciones para poder cambiar la contraseña.",
                    )
                    return redirect("home:index")
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="customers/password/password_reset.html",
        context={"password_reset_form": password_reset_form},
    )




