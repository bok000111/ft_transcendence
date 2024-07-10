from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreateModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        error_messages = {
            "email": {
                "unique": "Email already exists",
                "required": "Email required",
            },
            "username": {
                "unique": "Username already exists",
                "required": "Username required",
            },
            "password": {
                "required": "Password required",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["username"].required = True
        self.fields["password"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email, is_oauth_user=False).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username.isalnum() or len(username) > 12:
            raise forms.ValidationError(
                "Username can only contain alphanumeric characters"
            )
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
