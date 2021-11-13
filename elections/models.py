from django.conf import settings
from django.db import models

# Create your models here.

class Election(models.Model):
    position = models.CharField(verbose_name='position_for_which_election_is_conducted', max_length=128)
    deadline = models.DateTimeField(verbose_name='deadline_for_the_election')
    start_date = models.DateTimeField(verbose_name='start_date_of_the_election')
    end_date = models.DateTimeField(verbose_name='end_date_of_the_election')

    def __str__(self):
        return self.position + " - " + self.pk.__str__()

class Nomination(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User')
    election = models.ForeignKey(to=Election, on_delete=models.CASCADE, verbose_name='Election')

    class Type(models.IntegerChoices):
        CANDIDATE = 1
        VOTER = 2
    type_of_nomination = models.IntegerField(choices=Type.choices, verbose_name='Type of nomination')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'election', 'type_of_nomination'], name='each_user_can_have_one_entry_for_an_election')
        ]

    def __str__(self):
        return str(self.user) + " - " + str(self.election) + " - " + str(self.get_type_of_nomination_display())
