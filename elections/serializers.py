from rest_framework import serializers

from authentication.serializers import UserSerializer
from .models import Election, Nomination

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
