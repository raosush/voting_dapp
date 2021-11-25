from django.urls import path
from .views import CampaignView, FetchCampaignsView, FetchCandidatesOfElection, FetchCandidatures, FetchElectionView, FetchEligibleElections, VoteAPI

urlpatterns = [
   path('', FetchElectionView.as_view(), name='fetch_elections'),
   path('my_nominations', FetchCandidatures.as_view(), name='fetch_candidatures'),
   path('nominations', FetchCandidatesOfElection.as_view(), name='fetch_candidates_of_elections'),
   path('eligible_elections', FetchEligibleElections.as_view(), name='fetch_eligible_elections_for_which_a_user_is_eligible_to_vote'),
   path('campaigns', CampaignView.as_view(), name='create_or_update_campaigns'),
   path('campaigns/fetch', FetchCampaignsView.as_view(), name='fetch_campaigns'),
   path('vote', VoteAPI.as_view(), name='vote_for_a_candidate')
]
