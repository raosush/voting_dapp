from django.urls import path
from .views import FetchCandidatesOfElection, FetchCandidatures, FetchElectionView, FetchEligibleElections

urlpatterns = [
   path('', FetchElectionView.as_view(), name='fetch_elections'),
   path('my_nominations', FetchCandidatures.as_view(), name='fetch_candidatures'),
   path('nominations', FetchCandidatesOfElection.as_view(), name='fetch_candidates_of_elections'),
   path('eligible_elections', FetchEligibleElections.as_view(), name='fetch_eligible_elections_for_which_a_user_is_eligible_to_vote')
]
