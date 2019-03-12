from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.contrib.auth import login
from . import forms
from django.views.generic.edit import UpdateView
from braces.views import SelectRelatedMixin,LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from . import models


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

class Profile(SelectRelatedMixin, generic.DetailView):
    template_name = 'accounts/profile.html'
    select_related = ("skills", )

    def get_object(self):
        #import pdb;
        #pdb.set_trace()
        return get_object_or_404(models.User, pk=self.request.user.id)

@login_required
def ProfileEdit(request):
    user = get_object_or_404(models.User, pk=request.user.id)
    form = forms.UserForm(instance=user)
    if request.method == "POST":
        #import pdb;
        #pdb.set_trace()
        form = forms.UserForm(instance=user, data=request.POST,
                                     files=request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/profile_edit.html',
                          {'form': form})
    return render(request, 'accounts/profile_edit.html', {'form': form})



@login_required
def CreateSkill(request, pk):
    form = forms.SkillForm(instance=request.user)
    if request.method == "POST":
        form = forms.SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.save()
            form.save_m2m()
            return render(request, 'accounts/profile_edit.html',
                          {'form': form})
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def DeleteSkill(request,pk):            # meets the ajax request
    #import pdb;
    #pdb.set_trace()
    skill_id = int(request.POST['skill_id'])
    user = get_object_or_404(models.User, pk=int(request.POST['user_id']))
    #
    user.remove_item(skill_id)
    if user.is_empty():                   # if the last item is deleted
        user.untie(request.session)
        user.delete()
    return HttpResponse()