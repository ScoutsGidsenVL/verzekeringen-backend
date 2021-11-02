from rest_framework import serializers

from scouts_auth.models import MemberMedicalFlashCard

class MemberMedicalFlashCardSerializer(serializers.Serializer):

    class Meta:
        model = MemberMedicalFlashCard
        fields = "__all__"