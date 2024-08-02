from django.urls import path, include

from app.views import (IndexView,
                       EventsListView,
                       EventsDetailView,
                       LoginPage,
                       RegisterView,
                       sending_email,
                       verify_email_done,
                       verify_email_confirm,
                       verify_email_complete,
                       LogoutPage,
                       PeopleSave, ContactSave)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('events-lists/', EventsListView.as_view(), name='events-lists'),
    path('event-detail/<slug:slug>', EventsDetailView.as_view(), name='event-detail'),
    # Login and register
    path('login/', LoginPage.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutPage.as_view(), name='logout'),
    # verify
    path('sending-email-url/', sending_email, name='sending_email'),
    path('verify-email-done/', verify_email_done, name='verify_email_done'),
    path('verify-email-confirm/<uidb64>/<token>/', verify_email_confirm, name='verify_email_confirm'),
    path('verify-email-complete/', verify_email_complete, name='verify_email_complete'),
    path('people-save/', PeopleSave.as_view(), name='people_save'),
    path('contact-save/', ContactSave.as_view(), name='contact_save'), ]
