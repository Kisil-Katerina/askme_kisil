from django import forms
from django.contrib.auth.models import User
from django_select2.forms import Select2MultipleWidget
from .models import Profile, Question, Tag, Answer

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=25, label="NickName", 
                              widget=forms.TextInput(attrs={'class': 'form-control input-val','id': "username",'placeholder': 'Введите никнейм'}))
    
    email = forms.EmailField(label="Email", 
                            widget=forms.EmailInput(attrs={'class': 'form-control input-val','id': "email",'placeholder': 'Введите email'}))
    
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': 'form-control input-val','id': "password",'placeholder': 'Введите пароль'}))
    
    password2 = forms.CharField(label="Repeat password",
                               widget=forms.PasswordInput(attrs={'class': 'form-control input-val','id': "password2",'placeholder': 'Повторите пароль'}))
    
    avatar = forms.ImageField(label="Upload avatar", required=False,
                              widget=forms.FileInput(attrs={'class': 'form-control input-val file-input','type': "file",'id': "fileInput"}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
           self.add_error('username', "The user name must contain at least 5 characters")
        return username

    def clean(self):
        cleaned_data = super().clean()
        
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
           self.add_error('Password', "the entered passwords do not match")
           self.add_error('Password2', "the entered passwords do not match")
           
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username'] 
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password"])

        if commit:
           user.save()
           avatar = self.cleaned_data.get('avatar') # получаем файл
           Profile.objects.create(user=user, avatar=avatar) if avatar else Profile.objects.create(user=user)
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control input-val', 'placeholder': 'Введите никнейм'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control input-val', 'placeholder': 'Введите пароль'})
    )        
        
class UserSettingsForm(forms.Form):
    username = forms.CharField(max_length=25, label="NickName", 
                              widget=forms.TextInput(attrs={'class': 'form-control input-val','id': "username",'placeholder': 'Введите никнейм'}))
    
    email = forms.EmailField(label="Email",
                            widget=forms.EmailInput(attrs={'class': 'form-control input-val','id': "email",'placeholder': 'Введите email'}))
        
    avatar = forms.ImageField(label="Upload avatar", required=False,
                              widget=forms.FileInput(attrs={'class': 'form-control input-val file-input','type': "file",'id': "fileInput"}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
           self.add_error('username', "The user name must contain at least 5 characters")
        return username

class QuestionForm(forms.ModelForm):
    # используем поиск и множественный выбор
    tags = forms.CharField(
        widget=Select2MultipleWidget(attrs={'data-tags': 'true', 'data-token-separators': '[,]', 'class': 'form-control'}),
        required=False
    )
    
    class Meta:
        model = Question
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок', 'required': 'required'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст вопроса', 'rows': 4, 'required': 'required'}),
        }

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            tags = tags.strip('[]')  # удаляем квадратные скобки
            tags = tags.replace("'", "") # удаляем одинарные кавычки
            tags_list = tags.split(',')
            new_tags = []
            for tag_name in tags_list:
              tag_name = tag_name.strip()
              if tag_name.isdigit():  # проверяем, является ли tag_name числом (id)
                 try:
                    tag = Tag.objects.get(id=int(tag_name)) # если является, получаем тег по id
                    new_tags.append(tag)
                 except Tag.DoesNotExist: # Если id нет в бд
                    continue
              else:
                 tag, created = Tag.objects.get_or_create(name=tag_name) #если не является создаем
                 new_tags.append(tag)
            return new_tags
        return []
    
class AnswerForm(forms.ModelForm):
    
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите ваш ответ...', 
                                             'rows': 4, 'required': 'required', 'id':'content'}),
        }    