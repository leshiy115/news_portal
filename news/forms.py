
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group, AbstractUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext as _

from allauth.account.forms import SignupForm
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.forms import SignupForm as SocialSignupForm  # для переопределения метода первоначальной регистрации через гугл. Сменил наименование потому что выше есть такое же.

from .models import Post, Category, Author

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")
        if title == text:
            raise ValidationError({
                "text": _("The text should not be the same as the title.")
            })
        return cleaned_data



class BasicSignupForm(SignupForm):
    """Форма дополняющая регистрационную форму allauth новыми полями.
    Необходимо прописать путь в настройкахACCOUNT_FORMS = {'signup': 'news.forms.BasicSignupForm'}"""
    email = forms.EmailField(label="Email")
    username_validator = UnicodeUsernameValidator()
    username = forms.CharField(
        label=_('nickname'),
        max_length=150,
        validators=[username_validator],
        error_messages={
            "unique": _("A username with the same name already exists"),
        },
    )
    first_name = forms.CharField(label=_("Name"), required=False)
    last_name = forms.CharField(label=_("Surname"), required=False)

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


    def try_save(self, request):
        user, resp = super().try_save(request=request)
        return user, resp


    def save(self, request):
        # Автоматически добавляет всех пользователей в группу common
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        Author.objects.create(user=user)
        return user



# для переопределения метода первоначальной регистрации через гугл
##!! НЕ ПРОВЕРИЛ РАБОТОСПОСОБНОСТЬ ПОТОМУ ЧТО НЕ СДЕЛАЛ ДОПОЛНИТЕЛЬНОГО АККАУНТА ГУГЛ.
class MyCustomSocialSignupForm(SocialSignupForm):

    def save(self, request):
        user = super(MyCustomSocialSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        Author.objects.create(user=user)
        return user


class SubscriptionsForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            'subscriptions'
        ]

