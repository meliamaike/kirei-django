from django import forms
from .models import Customer
from django.contrib.auth import password_validation, login, authenticate
from allauth.account.forms import SignupForm, LoginForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column



#Form de registro
class RegisterForm(SignupForm):
    first_name = forms.CharField(label= "Nombre", max_length=30, required=True)
    last_name = forms.CharField(label = "Apellido", max_length=30, required=True)
    document_type = forms.ChoiceField(
    label = "Tipo de Documento",
    choices=[("", "Elegí una opción...")] + list(Customer.DOCUMENT_TYPE),
    required=True
)   
    document_number = forms.CharField(label = "Nro. Documento", max_length=30, required=True)
    email = forms.EmailField(max_length=255, required=True, label = "Email" )
    country_code = forms.CharField(label = "Código País", max_length=5, required=True)
    area_code = forms.CharField(label = "Código Área", max_length=5, required=True)
    phone_number = forms.CharField(label = "Nro. Teléfono", max_length=20, required=True)
    password1 = forms.CharField(label="Contraseña", strip=False)
    password2 = forms.CharField(label="Confirmá tu contraseña", strip=False)

    class Meta:
        model = Customer
        fields = [
            'first_name', 
            'last_name',
            'document_type',
            'document_number',
            'email',
            'country_code',
            'area_code',
            'phone_number',
            'password1',
            'password2'
        ]
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['email'].label = "Email"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmá tu contraseña"
        self.fields['password1'].widget.attrs['placeholder'] = ''
        self.fields['password2'].widget.attrs['placeholder'] = ''
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('document_type', css_class='form-group col-md-6'),
                Column('document_number', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'email',
            Row(
                Column('country_code', css_class='form-group col-md-6'),
                Column('area_code', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'phone_number',
            Row(
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),
            ),
            Submit('submit', 'Registrarme', css_class='btn-primary')
            )
  
    def save(self):
        if self.is_valid():
            data = self.cleaned_data
            customer = Customer.objects.create_user(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                document_type=data['document_type'],
                document_number=data['document_number'],
                country_code=data['country_code'],
                area_code=data['area_code'],
                phone_number=data['phone_number'],
                password=data['password1'],
            )
            customer.save()
            return customer

#Form de Login
class IngresarForm(LoginForm):
    remember = forms.BooleanField(required=False, widget=forms.CheckboxInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['login'].label = "Email"
        self.fields['password'].label = "Contraseña"
        self.fields['remember'].label = "Recuérdame"
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'login',
            'password',
            'remember',
        )
        
        self.fields['password'].widget.attrs['placeholder'] = ''
    
    def login(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None and user.is_active:
            # Login the user
            login(self.request, user)
        else:
            # Return an error message
            return self.add_error('email', 'Invalid email or password')

        return super(IngresarForm, self).login(*args, **kwargs)