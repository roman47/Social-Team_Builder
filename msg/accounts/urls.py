
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"index/$", views.Index.as_view(), name="index"),
    url(r"^$", views.Index.as_view(), name="index"),
    url(r"login/", views.LoginView.as_view(), name="login"),
    url(r"logout/", views.LogoutView.as_view(), name="logout"),
    url(r"signup/", views.SignUp.as_view(), name="signup"),
    url(r"profileView/$", views.ProfileView.as_view(), name="profile"),
    url(r'profile/(?P<pk>[0-9]+)/$', views.UserSkillUpdate.as_view(), name='profile-update'),
    url(r"projectNew/$", views.ProjectNew.as_view(), name="project-new"),
    url(r"project/(?P<pk>[0-9]+)/$", views.Project.as_view(), name="project"),
    url(r"projectEdit/(?P<pk>[0-9]+)/$", views.ProjectEdit.as_view(), name="project-edit"),
    url(r"applications/$", views.Applications.as_view(), name="applications"),
    url(r"search/$", views.search, name="search"),
    url(r"projectApply/(?P<pk>[0-9]+)/$", views.projectApply, name="project-apply"),
    url(r"projectByPosition/(?P<pk>[0-9]+)/$$", views.ProjectByPosition.as_view(), name="project-by-position"),
    url(r"applicantApprove/(?P<pk>[0-9]+)/$", views.applicantApprove, name="applicant-approve"),
    url(r"applicantReject/(?P<pk>[0-9]+)/$", views.applicantReject, name="applicant-reject"),
    url(r"messages/$", views.Messages.as_view(), name="messages"),
]

