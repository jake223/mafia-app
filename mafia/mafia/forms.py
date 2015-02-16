from django import forms

from models import *


class PlayerModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.user.username


class DeathReportForm(forms.Form):
    killer = PlayerModelChoiceField(
        queryset=Player.objects.filter(game__active=True),
        label='Who killed you?')
    kaboom = forms.BooleanField(
        initial=False, required=False,
        label="Was a kaboom used?")
    when = forms.IntegerField(label="How many minutes ago were you killed?")
    where = forms.CharField(label='Where were you killed?')


class KillReportForm(forms.Form):
    killed = PlayerModelChoiceField(
        queryset=Player.objects.filter(game__active=True, death=None),
        label='Who did you kill?')
    kaboom = forms.BooleanField(initial=False, required=False,
                                label="Was a kaboom used?")
    when = forms.IntegerField(label="How many minutes ago did this happen?")

    where = forms.CharField(label='Where did this happen?')

    mtp = forms.BooleanField(initial=False, required=False,
                             label="Manipulate the press?")


class DeathModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.murderee.user.username


class InvestigationForm(forms.Form):
    death = DeathModelChoiceField(
        queryset=Death.objects.filter(murderer__game__active=True),
        label="Which death would you like to investigate?",
    )
    guess = PlayerModelChoiceField(
        queryset=Player.objects.filter(game__active=True),
        label="Whom would you like to investigate?"
    )
    investigation_type = forms.ChoiceField(choices=Investigation.INVESTIGATION_KINDS,
                                           label="What kind of investigation are you using? [choose one you're allowed to]"
    )


class LynchVoteForm(forms.Form):
    vote = PlayerModelChoiceField(
        queryset=Player.objects.filter(game__active=True, death=None),
        label="Whom do you want to lynch?"
    )


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=30, label="Username (The same as on mafia.mit.edu, except for spaces)")
    password = forms.CharField(max_length=200, label="Password: ", widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=200, label="Confirm password: ", widget=forms.PasswordInput())
    email = forms.EmailField(max_length=50, label="Email Address:")
    game = forms.ModelChoiceField(
        queryset=Game.objects.filter(archived=False),
        label="Choose a game to join:"
    )
