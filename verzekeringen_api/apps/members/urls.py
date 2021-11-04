from rest_framework import routers

from apps.members.api.views import InuitsNonMemberViewSet, PersonSearch

router = routers.SimpleRouter()
router.register(r"non_member", InuitsNonMemberViewSet, "InuitsNonMember")
router.register(r"persons", PersonSearch, "PersonSearch")

urlpatterns = router.urls
