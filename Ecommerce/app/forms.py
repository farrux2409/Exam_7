from django import forms

from app.models import Event, Member, User, People, Contact
from app.authentication_form import AuthenticationForm


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ()


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)


class LoginForm(AuthenticationForm):
    email = forms.EmailField()
    password = forms.CharField(max_length=255)


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField()
    password = forms.CharField(max_length=255)
    confirm_password = forms.CharField(max_length=255)

    def clean_email(self):
        email = self.data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Bunday {email} allaqachon mavjud')
        return email

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password did not match')

        return password


class EmailForm(forms.Form):
    subject = forms.CharField(max_length=50)
    message = forms.CharField(widget=forms.Textarea)
    from_email = forms.EmailField()
    to = forms.EmailField()


# class OrderModelForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = ('costumer', 'phone_number')
class EmailPostForm(forms.Form):
    full_name = forms.CharField(max_length=25)
    email_address = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class PeopleForm(forms.ModelForm):
    class Meta:
        model = People
        exclude = ()


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ()
