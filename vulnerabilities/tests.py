from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from .models import Issue, Vulnerability
from .factories import IssueFactory, VulnerabilityFactory
from django.utils import timezone
from .serializers import IssueModelSerializer


class TestIssuesCSVUploadAPIView(APITestCase):
    def test_upload_valid_csv_file(self):
        csv = bytes(
            """ASSET - HOSTNAME,ASSET - IP_ADDRESS,VULNERABILITY - TITLE,VULNERABILITY - SEVERITY,VULNERABILITY - CVSS,VULNERABILITY - PUBLICATION_DATE
WORKSTATION-1,172.18.0.1,VMware ESXi 5.5 / 6.0 / 6.5 / 6.7 DoS (VMSA-2018-0018) (remote check),Médio,6.5,2018-07-19
WORKSTATION-2,172.18.0.2,VMware ESXi 5.5 / 6.0 / 6.5 / 6.7 DoS (VMSA-2018-0018) (remote check),Médio,6.5,2018-07-19
WORKSTATION-3,172.18.0.3,VMware ESXi 5.5 / 6.0 / 6.5 / 6.7 DoS (VMSA-2018-0018) (remote check),Médio,6.5,2018-07-19""",
            "utf-8",
        )
        file = SimpleUploadedFile("csv.csv", csv, content_type="text/plain")
        response = self.client.post(
            "/api/upload_csv/", {"file": file}, format="multipart"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Issue.objects.count() == 3
        assert Vulnerability.objects.count() == 1

    def test_upload_invalid_csv_file(self):
        csv = bytes("""""", "utf-8")
        file = SimpleUploadedFile("csv.csv", csv, content_type="text/plain")
        response = self.client.post(
            "/api/upload_csv/", {"file": file}, format="multipart"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_upload_nothing(self):
        response = self.client.post("/api/upload_csv/", format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestHostnamesResumeReportListAPIView(APITestCase):
    def test_hostnames_list(self):
        IssueFactory.create_batch(3)
        vulnerability = VulnerabilityFactory(cvss_score=100)
        issue = IssueFactory(vulnerability=vulnerability)
        response = self.client.get("/api/report/hostnames/")

        data = response.json()
        assert response.status_code == 200
        assert data["count"] == 4
        assert data["results"][0] == {
            "hostname": issue.hostname,
            "total": 1,
            "riskLevel": issue.vulnerability.cvss_score,
            "IpAddress": issue.ip_address,
        }


class TestResumeReportAPIView(APITestCase):
    def test_resume_list(self):
        issues = IssueFactory.create_batch(10)
        issues[0].fix_date = timezone.now()
        issues[0].save()
        response = self.client.get("/api/report/")
        data = response.json()

        cvss_list = map(lambda x: x.vulnerability.cvss_score, issues[1:10])

        assert response.status_code == 200
        assert data["stats"] == {
            "fixedIssuesCount": 1,
            "totalIssuesCount": 10,
            "hostnamesRiskAvg": round(sum(cvss_list) / 9, 2),
        }


class TestIssueReadOnlyModelViewSet(APITestCase):
    def test_list_all_issues(self):
        IssueFactory.create_batch(99)
        vulnerability = VulnerabilityFactory(cvss_score=100)
        issue = IssueFactory(vulnerability=vulnerability)
        response = self.client.get("/api/issues/")
        data = response.json()
        assert response.status_code == 200
        assert data["count"] == 100
        assert len(data["results"]) == 50
        assert data["results"][0] == IssueModelSerializer().to_representation(issue)


    def test_filter_hostname(self):
        IssueFactory.create_batch(99)
        vulnerability = VulnerabilityFactory(cvss_score=100)
        issue = IssueFactory(vulnerability=vulnerability)
        response = self.client.get(f"/api/issues/?hostname={issue.hostname}")
        data = response.json()
        assert response.status_code == 200
        assert data["count"] == 1


class TestToggleIssueResolution(APITestCase):
    def test_toggle_issue(self):
        issue = IssueFactory()
        response = self.client.post(f"/api/issues/toggle/{issue.id}/")
        updated_issue = Issue.objects.get(pk=issue.id)
        assert response.status_code == 200
        assert updated_issue.fix_date is not None
