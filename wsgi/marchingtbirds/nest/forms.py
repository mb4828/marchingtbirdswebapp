from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from models import Student, AuthenticationCode


class RegistrationForm(forms.Form):
    fname = forms.RegexField(regex=r'[A-Za-z]{1,30}', error_messages={'invalid': _("Must be fewer than 30 characters and only contain alphabet characters")}, label="Student's first name")
    lname = forms.RegexField(regex=r'[A-Za-z]{1,30}', error_messages={'invalid': _("Must be fewer than 30 characters and only contain alphabet characters")}, label="Student's last name")
    email = forms.EmailField(label='Student\'s e-mail address')
    username = forms.RegexField(regex=r'^([\w@+\-\.]){5,30}$', error_messages={'invalid': _("Usernames must contain at least 5 alphanumeric, _, @, +, . or - characters")},)
    password1 = forms.RegexField(regex=r'.{7,}', error_messages={'invalid': _("Password must contain at least 7 characters")}, label='Password', widget=forms.PasswordInput,)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Password again')
    authcode = forms.CharField(widget=forms.PasswordInput, label='Authentication code', max_length=40)
    privacy = forms.BooleanField(required=True, label='I have read and understand the <br/><a href="/privacy/" target="_blank">Marchingtbirds.tk privacy policy</a>')

    def clean_username(self):
        data = self.cleaned_data.get('username')

        if User.objects.filter(username=data):
            raise forms.ValidationError(_('This username is taken! Please try another.'))

        return data

    def clean_password1(self):
        data = self.cleaned_data.get('password1')

        if len(data) <= 7:
            raise forms.ValidationError(_('Password must contain at least 7 characters'))

        return data

    def clean_password2(self):
        data = self.cleaned_data.get('password2')
        p1 = self.cleaned_data.get('password1')

        if len(data) <= 7:
            return data

        if data != p1:
            raise forms.ValidationError(_('Passwords do not match'))

        return data

    def clean_authcode(self):
        data = self.cleaned_data.get('authcode')
        text = self.data.get('authcode')

        try:
            code = AuthenticationCode.objects.all()[0].code
        except:
            raise forms.ValidationError(_('Authentication code is invalid'))

        if text != code:
            raise forms.ValidationError(_('Authentication code is invalid'))

        return data

    def save(self, data):
        u = User.objects.create_user(data['username'], '', data['password1'])
        u.first_name = data['fname']
        u.last_name = data['lname']
        u.email = data['email']

        s = Student.objects.create(first_name=data['fname'], last_name=data['lname'], student_email=data['email'], user=u)

        u.save()
        s.save()
        return u

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['grad_year'].required = True
        self.fields['instrument'].required = True
        self.fields['tshirt'].required = True
        self.fields['student_email'].required = True
        self.fields['parent_email1'].required = True
        self.fields['parent_cell1'].required = True
        self.fields['street_address'].required = True
        self.fields['emergency_contact'].required = True
        self.fields['emergency_relationship'].required = True
        self.fields['emergency_phone'].required = True

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'grad_year', 'instrument', 'tshirt',
                  'student_email', 'parent_email1', 'parent_email2',
                  'home_phone', 'parent_cell1', 'parent_cell2', 'street_address',
                  'emergency_contact', 'emergency_relationship', 'emergency_phone',]
        labels = {
			'emergency_contact': _('Emergency contact name'),
		}
        widgets = {
            'grad_year': forms.TextInput(),
        }

class PasswordChangeForm(forms.Form):
    oldpass = forms.CharField(widget=forms.PasswordInput,label='Old password')
    newpass1 = forms.RegexField(regex=r'.{7,}', error_messages={'invalid': _("Password must contain at least 7 characters")}, label='Password', widget=forms.PasswordInput,)
    newpass2 = forms.CharField(widget=forms.PasswordInput, label='New password again')

    def clean_newpass1(self):
        data = self.cleaned_data.get('newpass1')

        if len(data) <= 7:
            raise forms.ValidationError(_('Password must contain at least 7 characters'))

        return data

    def clean_newpass2(self):
        data = self.cleaned_data.get('newpass2')
        p1 = self.cleaned_data.get('newpass1')

        if len(data) <= 7:
            return data

        if data != p1:
            raise forms.ValidationError(_('Passwords do not match'))

        return data