from rest_framework import serializers
from .models import Bin


class BinSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Bin
        fields = (
            'url', 'id', 'owner', 'date_created',
            'longitude', 'latitude', 'max_weight',
            'current_weight', 'fullness'
        )
        read_only_fields = (
            'date_created', 'fullness'
        )


class BinTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = ('token',)
        read_only_fields = ('token',)
