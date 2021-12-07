from django.db import models


class Vulnerability(models.Model):
    title = models.CharField(max_length=200, unique=True)
    cvss_score = models.FloatField()
    publication_date = models.DateField(blank=True, null=True)

    @property
    def severity(self) -> str:
        if self.cvss_score <= 3.9:
            return "Low"
        elif self.cvss_score <= 6.9:
            return "Medium"
        elif self.cvss_score <= 8.9:
            return "High"
        else:
            return "Critical"

    def __str__(self):
        return self.title


class Issue(models.Model):
    hostname = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=15)
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    fix_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.hostname}/{self.ip_address} - {self.vulnerability}"
