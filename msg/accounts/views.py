from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login
from . import forms
from django.views.generic.edit import UpdateView
from braces.views import SelectRelatedMixin,LoginRequiredMixin
from django.shortcuts import get_object_or_404, get_list_or_404,render
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import mixins
from rest_framework import generics

from . import models
from . import serializers


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("accounts:profile")
    template_name = "accounts/login.html"

    def get_form(self, form_class=None):
        #import pdb;
        #pdb.set_trace()
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        #import pdb;
        #pdb.set_trace()
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(generic.RedirectView):
    url = reverse_lazy("home")
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy("accounts:profile")


class ProfileView(SelectRelatedMixin, generic.DetailView):
    template_name = 'accounts/profile.html'
    select_related = ("skill", )

    def get_object(self):
        #import pdb;
        #pdb.set_trace()
        return get_object_or_404(models.User, pk=self.request.user.id)


class UserSkillUpdate(UpdateView):
    model = models.User
    fields = ['username', 'bio', 'avatar']
    success_url = reverse_lazy('accounts:profile')

    def get_context_data(self, **kwargs):
        data = super(UserSkillUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['skill'] = forms.SkillFormSet(self.request.POST, instance=self.object)
        else:
            data['skill'] = forms.SkillFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        skill = context['skill']
        with transaction.atomic():
            self.object = form.save()

            if skill.is_valid():
                skill.instance = self.object
                skill.save()
        return super(UserSkillUpdate, self).form_valid(form)


class ProjectNew(generic.CreateView):
    model = models.User
    form_class = forms.UserCreateForm
    template_name = 'accounts/project_new.html'
    success_url = reverse_lazy("home")


class ProjectEdit(generic.UpdateView):
    model = models.User
    form_class = forms.UserCreateForm
    template_name = 'accounts/project_edit.html'
    success_url = reverse_lazy("home")

class Project(generic.DetailView):
    model = models.User
    template_name = 'accounts/project.html'










class UserSkillCreate(generic.CreateView):
    model = models.User
    fields = ['username', 'bio', 'avatar']
    success_url = reverse_lazy('accounts:profile-list')

    def get_context_data(self, **kwargs):
        data = super(UserSkillCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['skill'] = forms.SkillFormSet(self.request.POST)
        else:
            data['skill'] = forms.SkillFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        skill = context['skill']
        with transaction.atomic():
            self.object = form.save()

            if skill.is_valid():
                skill.instance = self.object
                skill.save()
        return super(UserSkillCreate, self).form_valid(form)


class UserUpdate(UpdateView):
    model = models.User
    success_url = '/'
    fields = ['username', 'bio','avatar']








class ProfileList(generic.ListView):
    model = models.Profile


class ProfileCreate(generic.CreateView):
    model = models.Profile
    fields = ['first_name', 'last_name']


class ProfileFamilyMemberCreate(generic.CreateView):
    model = models.Profile
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('accounts:profile-list')

    def get_context_data(self, **kwargs):
        data = super(ProfileFamilyMemberCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['familymembers'] = forms.FamilyMemberFormSet(self.request.POST)
        else:
            data['familymembers'] = forms.FamilyMemberFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        familymembers = context['familymembers']
        with transaction.atomic():
            self.object = form.save()

            if familymembers.is_valid():
                familymembers.instance = self.object
                familymembers.save()
        return super(ProfileFamilyMemberCreate, self).form_valid(form)


class ProfileUpdate(UpdateView):
    model = models.Profile
    success_url = '/'
    fields = ['first_name', 'last_name']


class ProfileFamilyMemberUpdate(UpdateView):
    model = models.Profile
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('accounts:profile-list')

    def get_context_data(self, **kwargs):
        data = super(ProfileFamilyMemberUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['familymembers'] = forms.FamilyMemberFormSet(self.request.POST, instance=self.object)
        else:
            data['familymembers'] = forms.FamilyMemberFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        familymembers = context['familymembers']
        with transaction.atomic():
            self.object = form.save()

            if familymembers.is_valid():
                familymembers.instance = self.object
                familymembers.save()
        return super(ProfileFamilyMemberUpdate, self).form_valid(form)


class ProfileDelete(generic.DeleteView):
    model = models.Profile
    success_url = reverse_lazy('accounts:profile-list')