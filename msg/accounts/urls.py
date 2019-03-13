
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"login/", views.LoginView.as_view(), name="login"),
    url(r"logout/", views.LogoutView.as_view(), name="logout"),
    url(r"signup/", views.SignUp.as_view(), name="signup"),
    url(r"profileView/$", views.ProfileView.as_view(), name="profile"),
    url(r'profile/(?P<pk>[0-9]+)/$', views.UserSkillUpdate.as_view(), name='profile-update'),
    url(r"projectNew/$", views.ProjectNew.as_view(), name="project-new"),
    url(r"projectEdit/(?P<pk>[0-9]+)/$", views.ProjectEdit.as_view(), name="project-edit"),
    url(r"project/(?P<pk>[0-9]+)/$", views.Project.as_view(), name="project"),
    #url(r'profile/(?P<pk>[0-9]+)/delete/$', views.ProfileDelete.as_view(), name='profile-delete'),
    #url(r"profile_edit/", views.ProfileEdit, name="profile_edit"),
    #url(r"create_skill/(?P<pk>\d+)/$", views.CreateSkill.as_view(), name='create_skill'),
    #url(r'^$', views.ProfileList.as_view(), name='profile-list'),
    #url(r'profile/add/$', views.UserSkillCreate.as_view(), name='profile-add'),
]

