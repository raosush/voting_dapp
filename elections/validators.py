from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

def validate_candidate_nomination(nomination):
    if nomination.type_of_nomination != 1:
        raise ValidationError(_('You are not a candidate'))

def validate_campaign_time(nomination):
    if nomination.election.start_date < timezone.now():
        raise ValidationError(_('You cannot campaign now, since election has started!'))
