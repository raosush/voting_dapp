from rest_framework import serializers

from authentication.serializers import UserSerializer
from elections.validators import validate_campaign_time, validate_candidate_nomination
from .models import Campaign, Election, Nomination

class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = '__all__'

class NominationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    election = ElectionSerializer(read_only=True)
    type_of_nomination = serializers.CharField(source='get_type_of_nomination_display')

    class Meta:
        model = Nomination
        fields = "__all__"

class CampaignSerializer(serializers.ModelSerializer):
    nomination_id = serializers.PrimaryKeyRelatedField(queryset=Nomination.objects.all(), many=False, validators=[
        validate_campaign_time, validate_candidate_nomination])
    nomination = NominationSerializer(read_only=True)

    class Meta:
        model = Campaign
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class VoteSerializer(serializers.Serializer):
    nomination_id = serializers.PrimaryKeyRelatedField(queryset=Nomination.objects.all(), many=False)
