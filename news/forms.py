
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

from allauth.account.forms import SignupForm
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.forms import SignupForm as SocialSignupForm  # для переопределения метода первоначальной регистрации через гугл. Сменил наименование потому что выше есть такое же.

from .models import Post, Category


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
                "text": f"Текст не должен быть таким же как название."
            })
        return cleaned_data



class BasicSignupForm(SignupForm):
    """Форма дополняющая регистрационную форму allauth новыми полями.
    Необходимо прописать путь в настройкахACCOUNT_FORMS = {'signup': 'news.forms.BasicSignupForm'}"""
    print(f"\nСРАБОТАЛ  BasicSignupForm \n")
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)



    def save(self, request):
        # Автоматически добавляет всех пользователей в группу common
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user



# для переопределения метода первоначальной регистрации через гугл
##!! НЕ ПРОВЕРИЛ РАБОТОСПОСОБНОСТЬ ПОТОМУ ЧТО НЕ СДЕЛАЛ ДОПОЛНИТЕЛЬНОГО АККАУНТА ГУГЛ.
class MyCustomSocialSignupForm(SocialSignupForm):

    def save(self, request):
        user = super(MyCustomSocialSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user



