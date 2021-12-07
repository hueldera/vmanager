from rest_framework.serializers import (
    ModelSerializer,
    DateTimeField,
    BooleanField,
    FloatField,
    DateField,
    CharField,
    Serializer,
    IntegerField,
)
from .models import Issue, Vulnerability


class VulnerabilityModelSerializer(ModelSerializer):
    cvssScore = FloatField(source="cvss_score")
    publicationDate = DateField(source="publication_date")

    class Meta:
        model = Vulnerability
        fields = ("id", "title", "cvssScore", "publicationDate", "severity")


class IssueModelSerializer(ModelSerializer):
    vulnerability = VulnerabilityModelSerializer(many=False)
    createdAt = DateTimeField(source="created_at")
    fixDate = DateTimeField(source="fix_date")

    class Meta:
        model = Issue
        fields = ("id", "hostname", "createdAt", "fixDate", "vulnerability")


class HostnameResumeSerializer(Serializer):
    hostname = CharField()
    IpAddress = DateTimeField()
    total = IntegerField()
    riskLevel = FloatField()
