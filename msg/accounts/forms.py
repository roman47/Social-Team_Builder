
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
        model = models.Skills
        fields = '__all__'


def get_skills_formset(form, formset=BaseInlineFormSet, **kwargs):
    return inlineformset_factory(models.User, models.Skills, form,
                                formset, **kwargs)

SkillsFormSet = modelformset_factory(
    models.Skills,
    form=SkillForm,

)

SkillsInlineFormSet = inlineformset_factory(
    models.User,
    models.Skills,
    fields=('skill_name',),
    formset=SkillsFormSet,
    min_num=1,
    can_delete=True,
)

