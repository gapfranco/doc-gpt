from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    name = forms.CharField(label="Name", max_length=250)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password", widget=forms.PasswordInput)


class TopicForm(forms.Form):
    name = forms.CharField(label="Name", max_length=250)
    description = forms.CharField(label="Description", widget=forms.Textarea)
