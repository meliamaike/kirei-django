from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError



def index(request):
    #return render(request, "home/index.html")
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "email": form.cleaned_data["email_address"],
                "message": form.cleaned_data["message"],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, "admin@example.com", ["admin@example.com"])
            except BadHeaderError:
                return HttpResponse("Se encontró un header inválido.")
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, "home/index.html", {"form": form})