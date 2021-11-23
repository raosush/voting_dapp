from rest_framework import generics, status
from rest_framework.response import Response
from authentication.models import User
from elections.models import Campaign, Election, Nomination

from elections.serializers import CampaignSerializer, ElectionSerializer, NominationSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsOtpVerified
from .permissions import IsCampaignOwner

# Create your views here.

class FetchElectionView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = ElectionSerializer

    def get(self, request, format=None):
        return Response({"elections": ElectionSerializer(Election.objects.all(), context=self.get_serializer_context(), many=True).data}, status=status.HTTP_200_OK)

class FetchCandidatures(generics.GenericAPIView):
    serializer_class = NominationSerializer

    def get(self, request, format=None):
        return Response({"nominations": NominationSerializer(Nomination.objects.filter(user=request.user, type_of_nomination=1), context=self.get_serializer_context(), many=True).data}, status=status.HTTP_200_OK)

class FetchCandidatesOfElection(generics.GenericAPIView):
    permission_classes = []
    serializer_class = NominationSerializer

    def get(self, request, format=None):
        election_ids = request.GET.get('q', [])
        if type(election_ids) == list:
            return Response({"error": "Query parameter missing"}, status=status.HTTP_400_BAD_REQUEST)
        election_ids = election_ids.split(",")
        return Response({"nominations": NominationSerializer(Nomination.objects.filter(election__in=election_ids, type_of_nomination=1), context=self.get_serializer_context(), many=True).data}, status=status.HTTP_200_OK)

class FetchEligibleElections(generics.GenericAPIView):
    serializer_class = NominationSerializer

    def get(self, request, format=None):
        return Response({"nominations": NominationSerializer(Nomination.objects.filter(user=request.user, type_of_nomination=2), context=self.get_serializer_context(), many=True).data}, status=status.HTTP_200_OK)

class FetchCampaignsView(generics.GenericAPIView):
    serializer_class = CampaignSerializer
    permission_classes = []

    def get(self, request, format=None):
        type_of_query = request.GET.get('type', '')
        ids = request.GET.get('q', [])
        campaigns = []
        if type(ids) == list:
            return Response({"error": "Query parameter missing"}, status=status.HTTP_400_BAD_REQUEST)
        ids = ids.split(",")
        if type_of_query == 'user':
            user = User.objects.filter(pk__in=ids)
            nominations = Nomination.objects.filter(user__in=user)
            campaigns = Campaign.objects.filter(nomination__in=nominations)
        elif type_of_query == 'nomination':
            nominations = Nomination.objects.filter(pk__in=ids)
            campaigns = Campaign.objects.filter(nomination__in=nominations)
        elif type_of_query == '':
            campaigns = Campaign.objects.filter(pk__in=ids)
        else:
            return Response({"error": "Incorrect type parameter sent"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"campaigns": CampaignSerializer(campaigns, context=self.get_serializer_context(), many=True).data}, status=status.HTTP_200_OK)

class CampaignView(generics.GenericAPIView):
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated, IsOtpVerified, IsCampaignOwner]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        campaign = serializer.save()
        return Response({
            "campaign": CampaignSerializer(campaign, context=self.get_serializer_context()).data
        })

    def put(self, request, *args, **kwargs):
        try:
            campaign = Campaign.objects.get(user=request.user)
        except Campaign.DoesNotExist as e:
            return Response({"error": e.args}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, campaign)
        serializer = self.get_serializer(campaign, data=request.data)
        serializer.is_valid(raise_exception=True)
        campaign = serializer.save()
        return Response({
            "campaign": CampaignSerializer(campaign, context=self.get_serializer_context()).data
        })
