from rest_framework import generics, serializers, status
from rest_framework.response import Response
from elections.models import Election, Nomination

from elections.serializers import ElectionSerializer, NominationSerializer

# Create your views here.

class FetchElectionView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = ElectionSerializer

    def get(self, request, format=None):
        elections = []
        for election in Election.objects.all():
            elections.append(ElectionSerializer(election, context=self.get_serializer_context()).data)
        return Response({"elections": elections}, status=status.HTTP_200_OK)

class FetchCandidatures(generics.GenericAPIView):
    serializer_class = NominationSerializer

    def get(self, request, format=None):
        nominations = []
        for nomination in Nomination.objects.filter(user=request.user, type_of_nomination=1):
            nominations.append(NominationSerializer(nomination, context=self.get_serializer_context()).data)
        return Response({"nominations": nominations}, status=status.HTTP_200_OK)

class FetchCandidatesOfElection(generics.GenericAPIView):
    permission_classes = []
    serializer_class = NominationSerializer

    def get(self, request, format=None):
        election_ids = request.GET.get('q', [])
        if type(election_ids) == list:
            return Response({"error": "Query parameter missing"}, status=status.HTTP_400_BAD_REQUEST)
        election_ids = election_ids.split(",")
        nominations = []
        for nomination in Nomination.objects.filter(election__in=election_ids, type_of_nomination=1):
            nominations.append(NominationSerializer(nomination, context=self.get_serializer_context()).data)
        return Response({"nominations": nominations}, status=status.HTTP_200_OK)

class FetchEligibleElections(generics.GenericAPIView):
    serializer_class = NominationSerializer

    def get(self, request, format=None):
        nominations = []
        for nomination in Nomination.objects.filter(user=request.user, type_of_nomination=2):
            nominations.append(NominationSerializer(nomination, context=self.get_serializer_context()).data)
        return Response({"nominations": nominations}, status=status.HTTP_200_OK)
