
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory,ModelForm,modelformset_factory
from . import models


from django.forms.models import BaseInlineFormSet

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()
        
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"


class UserForm(ModelForm):
    class Meta:
        model = models.User
        fields = [
            'username',
            'avatar',
            'bio',
        ]


class SkillForm(ModelForm):
    class Meta:
        model = models.Skill
        fields = '__all__'


SkillFormSet = inlineformset_factory(models.User, models.Skill,
                                     form=SkillForm, extra=1)


class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'name',
        ]


ProjectFormSet = inlineformset_factory(models.User, models.Project,
                                       form=ProjectForm, extra=1)


class PositionForm(ModelForm):
    class Meta:
        model = models.Position
        fields = '__all__'


PositionFormSet = inlineformset_factory(models.Project, models.Position,
                                       form=PositionForm, extra=1)












class ProfileForm(ModelForm):
    class Meta:
        model = models.Profile
        exclude = ()


class FamilyMemberForm(ModelForm):
    class Meta:
        model = models.FamilyMember
        exclude = ()


FamilyMemberFormSet = inlineformset_factory(models.Profile, models.FamilyMember,
form=FamilyMemberForm, extra=1)