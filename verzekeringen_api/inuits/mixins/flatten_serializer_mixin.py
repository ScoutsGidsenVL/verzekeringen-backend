class FlattenSerializerMixin(object):
    """
    Flatten nested serializer data by adding a flatten property in Meta

    @see https://stackoverflow.com/a/41418576
    """

    def __init__(self, *args, **kwargs):
        # self.allowed_fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

    def to_representation(self, obj):
        """
        Move fields from nested serializers to root if Meta.flatten is set
        """
        representation = super().to_representation(obj)

        if hasattr(self.Meta, "flatten"):
            for field, serializer_class in self.Meta.flatten:
                serializer = serializer_class(context=self.context)
                objrep = serializer.to_representation(getattr(obj, field))

                for key in objrep:
                    # if key in representation:
                    #     raise ValidationError(
                    #         "A field with name '" + key + "' already exists")
                    # representation[field + "__" + key] = objrep[key]
                    # representation[key] = objrep[key]
                    if key in representation:
                        representation[field + "__" + key] = objrep[key]
                    else:
                        representation[key] = objrep[key]

        return representation

    def to_internal_value(self, data):

        # remove flattened nested keys
        nested_fields = {}
        if hasattr(self.Meta, "flatten"):
            for field, serializer_class in self.Meta.flatten:
                serializer = serializer_class(context=self.context)
                serializer_fields = serializer.Meta.fields
                serializer_internal = {}
                for key in serializer_fields:
                    if key in data:
                        serializer_internal[key] = data.pop(key)
                nested_fields[field] = serializer_internal

        internal_values = super().to_internal_value(data)
        for key in nested_fields:
            internal_values[key] = nested_fields[key]

        return internal_values
