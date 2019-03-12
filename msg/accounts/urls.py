
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"login/", views.LoginView.as_view(), name="login"),
    url(r"logout/", views.LogoutView.as_view(), name="logout"),
    url(r"signup/", views.SignUp.as_view(), name="signup"),
    url(r"profile/", views.Profile.as_view(), name="profile"),
    url(r"profile_edit/", views.ProfileEdit, name="profile_edit"),
    url(r'^create_skill/(?P<pk>\d+)/$', views.CreateSkill, name='create_skill'),
]

