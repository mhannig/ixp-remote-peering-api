
from rest_framework import serializers

from remote_peering import models


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ('id', 'name', 'created_at')


class AsSerializer(serializers.ModelSerializer):
    member = MemberSerializer(source='member_set', many=True)

    class Meta:
        model = models.As
        fields = ('id', 'number', 'created_at', 'member')
        depth = 1


class IxpSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = models.Ixp
        fields = ('id', 'name', 'members', 'locations', 'peeringdb_id')
        depth = 2


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ('id', 'continent', 'country', 'city')


class IpSerializer(serializers.ModelSerializer):
    member = MemberSerializer()

    class Meta:
        model = models.Ip
        fields = ('id', 'address', 'version', 'longitude', 'latitude',
                  'member', 'locations', 'created_at')
        depth = 2


class IpMetricSerializer(serializers.ModelSerializer):
    ip = IpSerializer()

    class Meta:
        model = models.IpMetric
        fields = ('id', 'ip', 'median_rtt', 'created_at')
        depth = 2
