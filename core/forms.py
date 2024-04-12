from django import forms

from core.models import Topic, User
from core.utils.text_extractor import check_text


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    name = forms.CharField(label="Name", max_length=250)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password", widget=forms.PasswordInput)


class TopicForm(forms.Form):
    name = forms.CharField(label="Name", max_length=250, initial="")
    description = forms.CharField(
        label="Description", widget=forms.Textarea, initial=""
    )
    type = forms.ChoiceField(label="Tipo", choices=Topic.TOPIC_TYPES)


class ProfileForm(forms.Form):
    name = forms.CharField(label="Name", max_length=250)
    preferred_language = forms.ChoiceField(
        label="Preferred Language", choices=User.LANGUAGE_CHOICES
    )
    query_balance = forms.IntegerField()
    query_credits = forms.IntegerField()


class DocumentForm(forms.Form):
    file = forms.FileField(label="File")
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(), label="Topic", required=False
    )

    def clean_file(self):
        file = self.cleaned_data["file"]
        max_size = 30
        if file.size > max_size * 1024 * 1024:
            raise forms.ValidationError(
                f"Arquivo muito grande. Máximo é {max_size}MB"
            )
        file_type = check_text(file)
        if not file_type:
            raise forms.ValidationError(
                "Apenas arquivos texto, PDF ou Word são permitidos."
            )
        if file_type == "pdf error":
            raise forms.ValidationError("PDF inválido ou danificado")
        return file


class QuestionForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea)


class InviteForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
