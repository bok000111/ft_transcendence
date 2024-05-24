from django import forms
from django.conf import settings
from django.db import transaction
from channels.db import database_sync_to_async

from . import models


class LobbyCreateModelForm(forms.ModelForm):
    class Meta:
        model = models.GameLobby
        fields = ["name", "max_players", "end_score"]
        labels = {
            "name": "Lobby name",
            "max_players": "Maximum player count",
            "end_score": "End score",
        }
        error_messages = {
            "name": {
                "required": "Lobby name is required",
                "max_length": "Lobby name is too long",
            },
            "max_players": {
                "min_value": "Maximum player count must be at least 2",
                "max_value": "Maximum player count must be at most 4",
            },
            "end_score": {
                "min_value": "End score must be at least 1",
                "max_value": "End score must be at most 10",
            },
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["max_players"].required = False
        self.fields["end_score"].required = False

    def clean_max_players(self):
        max_players = self.cleaned_data["max_players"]
        if max_players is None:
            return 2
        if max_players < 2:
            raise forms.ValidationError(
                self.fields["max_players"].error_messages["min_value"], code="invalid"
            )
        if max_players > 4:
            raise forms.ValidationError(
                self.fields["max_players"].error_messages["max_value"], code="invalid"
            )
        return max_players

    def clean_end_score(self):
        end_score = self.cleaned_data["end_score"]
        if end_score is None:
            return 10
        if end_score < 1:
            raise forms.ValidationError(
                self.fields["end_score"].error_messages["min_value"], code="invalid"
            )
        if end_score > 10:
            raise forms.ValidationError(
                self.fields["end_score"].error_messages["max_value"], code="invalid"
            )
        return end_score

    @transaction.atomic
    def save(self, commit=True):
        lobby = super().save(commit=False)
        if commit:
            lobby.save()
            lobby.players.add(self.user, through_defaults={"is_host": True})
            lobby.player_count = 1
            lobby.save()
        return lobby

    @database_sync_to_async
    def asave(self):
        return self.save()


class NicknameForm(forms.Form):
    nickname = forms.CharField(
        label="Nickname",
        max_length=12,
        min_length=2,
        error_messages={
            "required": "Nickname is required",
            "min_length": "Nickname must be at least 2 characters long",
            "max_length": "Nickname must be at most 12 characters long",
        },
    )

    def clean_nickname(self):
        nickname = self.cleaned_data["nickname"]
        if not nickname.isalnum():
            raise forms.ValidationError(
                "Nickname must contain only letters and numbers"
            )
        return nickname
