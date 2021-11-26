import logging

from rest_framework import serializers

from apps.people.models import InuitsAbstractPerson


logger = logging.getLogger(__name__)


class InuitsAbstractPersonSerializer(serializers.ModelSerializer):
    # first_name    max_length=15           required
    # last_name     max_length=25           required
    # phone_number  max_length=15           optional
    # birth_date    date                    optional
    # gender        choices=Gender.choices  optional
    # street        max_length=100          optional
    # number        max_length=5            optional
    # letter_box    max_length=5            optional
    # postal_code   number                  optional
    # city          max_length=40           optional
    # comment       max_length=500          optional

    class Meta:
        model = InuitsAbstractPerson
        fields = "__all__"
