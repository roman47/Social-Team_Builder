from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login
from . import forms
from django.views.generic.edit import UpdateView
from braces.views import SelectRelatedMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction

import re
from django.db.models import Q
from django.template import RequestContext

from . import models
from . import serializers
from .filters import ProjectFilter


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("accounts:messages")
    template_name = "accounts/login.html"

    def get_form(self, form_class=None):
        # import pdb;
        # pdb.set_trace()
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        # import pdb;
        # pdb.set_trace()
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
    success_url = reverse_lazy("accounts:index")


class ProfileView(SelectRelatedMixin, generic.DetailView):
    template_name = 'accounts/profile.html'
    select_related = ("skill",)

    def get_object(self):
        # import pdb;
        # pdb.set_trace()
        return get_object_or_404(models.User, pk=self.request.user.id)


class UserSkillUpdate(UpdateView):
    model = models.User
    fields = ['username', 'bio', 'avatar']
    success_url = reverse_lazy('accounts:profile')

    def get_context_data(self, **kwargs):
        data = super(UserSkillUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['skill'] = forms.SkillFormSet(self.request.POST,
                                               instance=self.object)
            data['project'] = forms.ProjectFormSet(self.request.POST,
                                                   instance=self.object)
        else:
            data['skill'] = forms.SkillFormSet(instance=self.object)
            data['project'] = forms.ProjectFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        skill = context['skill']
        project = context['project']
        with transaction.atomic():
            self.object = form.save()
            if skill.is_valid():
                skill.instance = self.object
                skill.save()
            if project.is_valid():
                project.instance = self.object
                project.save()
        return super(UserSkillUpdate, self).form_valid(form)


class Project(generic.DetailView):
    template_name = 'accounts/project.html'
    select_related = ("position",)

    def get_object(self):
        # import pdb;
        # pdb.set_trace()
        return get_object_or_404(models.Project,
                                 pk=self.kwargs.get('pk', None))
    def get_context_data(self, **kwargs):
        context = super(Project, self).get_context_data(
            **kwargs)  # get the default context data
        context['applicants'] = models.Applicant.objects.all()
        return context


class ProjectEdit(UpdateView):
    model = models.Project
    fields = '__all__'

    def get_success_url(self):
        id = self.kwargs['pk']
        return reverse_lazy('accounts:project', kwargs={'pk': id})

    def get_context_data(self, **kwargs):
        data = super(ProjectEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['position'] = forms.PositionFormSet(self.request.POST,
                                                     instance=self.object)
        else:
            data['position'] = forms.PositionFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        position = context['position']
        with transaction.atomic():
            self.object = form.save()
            if position.is_valid():
                position.instance = self.object
                position.save()
        return super(ProjectEdit, self).form_valid(form)


class ProjectNew(generic.CreateView):
    model = models.Project
    template_name = 'accounts/project_new.html'
    fields = '__all__'
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        data = super(ProjectNew, self).get_context_data(**kwargs)
        if self.request.POST:
            data['position'] = forms.PositionFormSet(self.request.POST)
        else:
            data['position'] = forms.PositionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        position = context['position']
        with transaction.atomic():
            self.object = form.save()

            if position.is_valid():
                position.instance = self.object
                position.save()
        return super(ProjectNew, self).form_valid(form)


class Applications(generic.ListView):
    model = models.Applicant

    def get_queryset(self):
        user_id = self.request.user.id
        project_ids = models.Project.objects.filter(owner=user_id)
        position_ids = models.Position.objects.filter(project_id__in=project_ids)
        queryset = models.Applicant.objects.filter(position_id__in=position_ids)
        #import pdb;
        #pdb.set_trace()
        return queryset

class Index(generic.ListView):
    model = models.Project
    template_name = 'accounts/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(
            **kwargs)  # get the default context data
        context['positions'] = models.Position.objects.all()
        return context


def search(request):
    project_list = models.Project.objects.all()
    project_filter = ProjectFilter(request.GET, queryset=project_list)
    positions_all = models.Position.objects.all()
    # import pdb;
    # pdb.set_trace()
    return render(request, 'accounts/index.html',
                  {'filter': project_filter, 'positions': positions_all})


def projectApply(request,pk):
    new_applicant, created = models.Applicant.objects.get_or_create(position_id=pk,
                                     user_id=request.user.id)
    new_applicant.save()
    project_id = new_applicant.position.project.id
    #import pdb;
    #pdb.set_trace()
    return redirect('accounts:project', pk=project_id)


class ProjectByPosition(generic.DetailView):
    model = models.Project
    template_name = 'accounts/index.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectByPosition, self).get_context_data(
            **kwargs)  # get the default context data
        context['positions'] = models.Position.objects.all()
        return context


def applicantApprove(request, pk):
    models.Applicant.objects.filter(pk=pk).update(accepted=True)
    return redirect('accounts:applications')


def applicantReject(request, pk):
    models.Applicant.objects.filter(pk=pk).update(accepted=False)
    return redirect('accounts:applications')


class Messages(generic.ListView):
    model = models.Applicant

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = models.Applicant.objects.filter(user_id=user_id).filter(accepted__isnull=False)
        return queryset