from rest_framework import serializers

from locations.models import Location


class LocationListSerializer(serializers.ModelSerializer):
    # authors = serializers.StringRelatedField(many=True)
    # publisher = serializers.StringRelatedField()
    class Meta:
        model = Location
        fields = ('eatery_name',)

    def build_field(self, field_name, info, model_class, nested_depth):
        return super(LocationListSerializer, self).build_field(field_name, info, model_class, nested_depth)

    # def to_representation(self, instance):
    #     """Convert `username` to lowercase."""
    #     ret = super(BooksListSerializer, self).to_representation(instance)
    #     # ret['authors'] = ret['username'].lower()
    #     # return ret