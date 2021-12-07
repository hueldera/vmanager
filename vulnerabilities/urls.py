from django.urls import path
from rest_framework.routers import SimpleRouter
from .api import (
    IssuesCSVUploadAPIView,
    IssueReadOnlyModelViewSet,
    ResumeReportAPIView,
    HostnamesResumeReportListAPIView,
    toggle_issue_resolution,
)

router = SimpleRouter()
router.register("issues", IssueReadOnlyModelViewSet)

urlpatterns = [
    path("upload_csv/", IssuesCSVUploadAPIView.as_view(), name="issues_csv_upload"),
    path("report/", ResumeReportAPIView.as_view(), name="report"),
    path(
        "report/hostnames/",
        HostnamesResumeReportListAPIView.as_view(),
        name="report_hostnames",
    ),
    path("issues/toggle/<int:id>/", toggle_issue_resolution, name="issues_toggle"),
] + router.urls
