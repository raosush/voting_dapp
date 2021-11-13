from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
import csv

from authentication.models import User
from elections.models import Election, Nomination


class CsvImportForm(forms.Form):
    csv_file = forms.FileField(
        label='Upload a CSV to bulk import candidates and voters', widget=widgets.FileInput)

    def save(self):
        file_data = self.cleaned_data["csv_file"].read().decode(
            'utf-8').split("\n")
        email = [line[0] for line in csv.reader(file_data)]
        election_id = [int(line[1]) for line in csv.reader(file_data)]
        users = list(User.objects.filter(email__in=email))
        elections = list(Election.objects.filter(pk__in=election_id))
        for line in csv.reader(file_data):
            if len(line) == 3:
                nomination = Nomination(user=[x for x in users if x.email == line[0]][0],
                                        election=[x for x in elections if x.id == int(line[1])][0],
                                        type_of_nomination=line[2])
                nomination.full_clean()
                nomination.save()
