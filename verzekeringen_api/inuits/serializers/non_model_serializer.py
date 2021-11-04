import logging

from rest_framework import serializers


logger = logging.getLogger(__name__)


class NonModelSerializer(serializers.BaseSerializer):
    def get_object():
        raise NotImplementedError("The get_object method should be implemented in a concrete subclass.")

    def to_internal_value(self, data):
        """BaseSerializer instances must implement this to support read operations."""
        raise NotImplementedError("The to_internal_value method should be implemented in a concrete subclass.")

    def to_representation(self, instance):
        """
        BaseSerializer instances must implement this to support write operations.

        @see https://www.django-rest-framework.org/api-guide/serializers/#creating-new-base-classes
        """
        # raise NotImplementedError("The to_representation method should be implemented in a concrete subclass.")
        output = {}
        for attribute_name in dir(instance):
            attribute = getattr(instance, attribute_name)
            if attribute_name.startswith("_"):
                # Ignore private attributes.
                pass
            elif hasattr(attribute, "__call__"):
                # Ignore methods and other callables.
                pass
            elif isinstance(attribute, (str, int, bool, float, type(None))):
                # Primitive types can be passed through unmodified.
                output[attribute_name] = attribute
            elif isinstance(attribute, list):
                # Recursively deal with items in lists.
                output[attribute_name] = [self.to_representation(item) for item in attribute]
            elif isinstance(attribute, dict):
                # Recursively deal with items in dictionaries.
                output[attribute_name] = {str(key): self.to_representation(value) for key, value in attribute.items()}
            else:
                # Force anything else to its string representation.
                output[attribute_name] = str(attribute)

        return output
