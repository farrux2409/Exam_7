from datetime import datetime
from lib2to3.fixes.fix_input import context

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, View, FormView

from app.models import Event
from app.forms import MemberForm, ContactForm, RegisterForm, PeopleForm

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from app.forms import LoginForm
from app.models import User
from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL

# email verify
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
# from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from app.tokens import account_activation_token
from app.forms import EmailForm


# Create your views here.


class IndexView(View):

    def get(self, request):
        form = MemberForm()

        return render(request, 'app/index.html', {'form': form, })

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

        return render(request, 'app/index.html', {'form': form})


class EventsListView(ListView):
    template_name = 'app/event-listing.html'
    model = Event
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = datetime.now()

        # Filter upcoming events (events in the future)
        upcoming_events = Event.objects.filter(created_at__gte=now).order_by('-created_at')[:2]

        # Filter past events (events in the past)
        latest_events = Event.objects.filter(created_at__lt=now).order_by('created_at')

        # Add the events to the context
        context['upcoming_events'] = upcoming_events
        context['latest_events'] = latest_events

        return context


class EventsDetailView(TemplateView):
    template_name = 'app/event-detail.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        event = Event.objects.get(slug=self.kwargs['slug'])
        contex['event'] = event
        return contex


# def detail(request, slug):
#     context = {}
#     temp = Event.objects.filter(slug=slug)
#     context['event'] = temp
#     return render(request, 'app/detail.html', context)


""" class CustomLoginView(LoginView):
    template_name = 'app/auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def form_invalid(self, form):
        if form.errors:
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                if not user.check_password(form.cleaned_data['password']):
                    messages.add_message(self.request, messages.ERROR, 'Password didn\'t match.')
            except User.DoesNotExist:
                messages.add_message(request=self.request, level=messages.ERROR, message='User not found')

        return self.render_to_response(self.get_context_data(form=form)) """


class LoginPage(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'app/auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
            else:
                messages.add_message(
                    request,
                    level=messages.WARNING,
                    message='User not found'
                )

        return render(request, 'app/auth/login.html', {'form': form})


""" class RegisterFormView(FormView):
    template_name = 'app/auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        first_name = form.cleaned_data.get('first_name')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = User.objects.create_user(first_name=first_name, email=email, password=password)
        user.is_active = False
        user.is_staff = True
        user.is_superuser = True
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Verify your account '
        message = render_to_string('app/auth/email/activation.html',
                                   {
                                       'request': self.request,
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.id)),
                                       'token': account_activation_token.make_token(user)
                                   })

        email = EmailMessage(subject, message, to=[email])
        email.content_subtype = 'html'
        email.send()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('verify_email_done') """


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'app/auth/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(first_name=first_name, email=email, password=password)
            user.is_active = False
            user.is_staff = True
            user.is_superuser = True
            user.save()

            current_site = get_current_site(request)
            subject = 'Verify your email'
            message = render_to_string('app/auth/email/activation.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(subject, message, to=[email])
            email.content_subtype = 'html'
            email.send()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('verify_email_done')

        return render(request, 'app/auth/register.html', {'form': form})


class LogoutPage(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('index'))

    def post(self, request):
        return render(request, 'app/auth/logout.html')


def sending_email(request):
    sent = False

    if request.method == 'POST':
        form = EmailForm(request.POST)
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = request.POST.get('from_email')
        to = request.POST.get('to')
        send_mail(subject, message, from_email, [to])
        sent = True

    return render(request, 'app/auth/sending-email.html', {'form': form, 'sent': sent})


def verify_email_done(request):
    return render(request, 'app/auth/email/verify-email-done.html')


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect('verify_email_complete')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'app/auth/email/verify-email-confirm.html')


def verify_email_complete(request):
    return render(request, 'app/auth/email/verify-email-complete.html')


class PeopleSave(View):
    def get(self, request):
        form = PeopleForm()
        return render(request, 'app/index.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PeopleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

        return render(request, 'app/index.html', {'form': form})


class ContactSave(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'app/index.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

        return render(request, 'app/index.html', {'form': form})
