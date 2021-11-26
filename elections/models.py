from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User

from elections.validators import validate_campaign_time, validate_candidate_nomination
import hashlib
from django.core.mail import send_mail

# Create your models here.

class Election(models.Model):
    position = models.CharField(verbose_name='position_for_which_election_is_conducted', max_length=128)
    deadline = models.DateTimeField(verbose_name='deadline_for_the_election')
    start_date = models.DateTimeField(verbose_name='start_date_of_the_election')
    end_date = models.DateTimeField(verbose_name='end_date_of_the_election')
    vote_count = models.JSONField(verbose_name='dict_of_vote_count', default=dict)

    def cast_vote(self, voter_id, candidate_id):
        self.vote_for_candidate(voter_id, candidate_id, self.id, Vote.objects.filter(election=self).last())
        self.vote_count[str(candidate_id)] += 1
        self.save()

    def vote_for_candidate(self, voter_id, candidate_id, election_id, prev_vote):
        sha_hash = hashlib.sha256()
        data = prev_vote.data or ''
        while True:
            string = str(data) + str(voter_id) + str(candidate_id) + str(election_id) + str(prev_vote.created_at) + str(prev_vote.updated_at)
            sha_hash.update('{}'.format(string).encode())
            if sha_hash.hexdigest().find(str(candidate_id)) != -1:
                return Vote.objects.create(data=sha_hash.hexdigest(),
                 election=Election.objects.get(pk=election_id), candidate=User.objects.get(pk=candidate_id),
                 voter=User.objects.get(pk=voter_id))

    def __str__(self):
        return self.position + " - " + self.pk.__str__()

@receiver(post_save, sender=Election, dispatch_uid='initialize_vote_count_for_election')
def after_adding_election(sender, instance, **kwargs):
    if kwargs['created']:
        sha_hash = hashlib.sha256()
        sha_hash.update('{}'.format(instance.id).encode())
        Vote.objects.create(data=sha_hash.hexdigest(), election=instance)
        instance.vote_count = dict()
        instance.save()
        send_mail(subject='Voting Dapp - New election added', message='A new election has been added on our platform. Check it out now!',
        from_email=settings.EMAIL_HOST_USER, to=[x.email for x in User.objects.filter(is_active=True, is_admin=False)])

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

@receiver(post_save, sender=Nomination, dispatch_uid='initialize_vote_count_for_candidate')
def after_adding_candidate(sender, instance, **kwargs):
    if instance.type_of_nomination == 1 and kwargs['created']:
        temp = instance.election
        temp.vote_count[instance.user.id.__str__()] = 0
        temp.save()
        send_mail(subject='Voting Dapp - Nomination filed', message='Your nomination as a candidate has been filed for %s' %(temp.position),
        from_email=settings.EMAIL_HOST_USER, recipient_list=[instance.user.email])
    elif instance.type_of_nomination == 2 and kwargs['created']:
        send_mail(subject='Voting Dapp - Eligible Voter', message='You are an eligible voter in the election %s' %(instance.election.position),
        from_email=settings.EMAIL_HOST_USER, recipient_list=[instance.user.email])

class Vote(models.Model):
    election = models.ForeignKey(to=Election, on_delete=models.CASCADE, verbose_name='Election')
    voter = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='voter', verbose_name='Voter', null=True)
    candidate = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='candidate', verbose_name='Candidate', null=True)
    data = models.TextField(verbose_name='sha_512_256_generated_hash')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['voter', 'election'], name='each_user_can_have_one_vote_for_an_election')
        ]

class Campaign(models.Model):
    campaign = models.TextField(verbose_name='campaign_of_a_candidate', max_length=65535)
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, related_name='campaigns', validators=[
        validate_campaign_time, validate_candidate_nomination])

    def __str__(self):
        return str(self.nomination.user) + " - " + str(self.pk)
