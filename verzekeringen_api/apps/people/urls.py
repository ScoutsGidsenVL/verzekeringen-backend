from apps.people.views import InuitsNonMemberViewSet, PersonSearch
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"non_member", InuitsNonMemberViewSet, "InuitsNonMember")
router.register(r"persons", PersonSearch, "PersonSearch")

urlpatterns = router.urls
