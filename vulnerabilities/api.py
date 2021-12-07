from typing import List
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework import status
from .serializers import IssueModelSerializer, HostnameResumeSerializer
from django.db import transaction
from django.db.models import Count, Max, F, Avg
import logging
import pandas as pd
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Vulnerability, Issue


logger = logging.getLogger(__name__)


def toggle_issue_resolution(request, id):
    issue = Issue.objects.get(id=id)
    if issue.fix_date is None:
        issue.fix_date = timezone.now()
    else:
        issue.fix_date = None

    issue.save()
    return HttpResponse()


class IssueReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = (
        Issue.objects.select_related("vulnerability")
        .all()
        .order_by("-vulnerability__cvss_score")
    )
    serializer_class = IssueModelSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["hostname", "ip_address"]


class ResumeReportAPIView(APIView):
    def get(self, request):
        issues = Issue.objects.select_related("vulnerability").all()
        fixed_issues_count = issues.filter(fix_date__isnull=False).count()
        hostnames_risk_avg = issues.filter(fix_date__isnull=True).aggregate(
            risk_avg=Avg("vulnerability__cvss_score")
        )
        issues_count = issues.count()

        return Response(
            {
                "stats": {
                    "fixedIssuesCount": fixed_issues_count,
                    "totalIssuesCount": issues_count,
                    "hostnamesRiskAvg": round(hostnames_risk_avg["risk_avg"], 2),
                },
            },
            status=status.HTTP_200_OK,
        )


class HostnamesResumeReportListAPIView(ListAPIView):
    queryset = (
        Issue.objects.select_related("vulnerability")
        .filter(fix_date__isnull=True)
        .values("hostname")
        .annotate(IpAddress=F("ip_address"))
        .annotate(total=Count("hostname"))
        .annotate(riskLevel=Max("vulnerability__cvss_score"))
        .order_by("-riskLevel", "-total")
    )
    serializer_class = HostnameResumeSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["hostname", "ip_address"]


class IssuesCSVUploadAPIView(APIView):
    @transaction.atomic
    def post(self, request):
        csvfile = request.FILES.get("file")
        issues = []
        vulnerability_cache = {}

        try:
            df = pd.read_csv(csvfile, dtype=str, na_filter=False)
        except Exception as e:
            logger.error(e)
            return Response(
                {"error": "Invalid CSV file."}, status=status.HTTP_400_BAD_REQUEST
            )

        for (
            _,
            hostname,
            ip_address,
            title,
            severity,
            cvss_score,
            publication_date,
        ) in df.itertuples():
            if title not in vulnerability_cache:
                publication_date = publication_date if publication_date != "" else None
                cvss_score = cvss_score if cvss_score != "" else 0
                vulnerability, _ = Vulnerability.objects.get_or_create(
                    title=title,
                    cvss_score=cvss_score,
                    publication_date=publication_date,
                )
                vulnerability_cache[title] = vulnerability
            else:
                vulnerability = vulnerability_cache[title]

            issues.append(
                Issue(
                    hostname=hostname,
                    ip_address=ip_address,
                    vulnerability=vulnerability,
                )
            )

        Issue.objects.bulk_create(issues)

        return Response(status=status.HTTP_201_CREATED)
