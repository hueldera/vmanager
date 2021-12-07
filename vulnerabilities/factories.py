from factory.declarations import SubFactory, Sequence
from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory import LazyFunction
from datetime import datetime
import random
from vulnerabilities.models import Vulnerability


class VulnerabilityFactory(DjangoModelFactory):
    class Meta:
        model = "vulnerabilities.Vulnerability"

    title = Sequence(lambda n: 'Title {0}'.format(n))
    cvss_score = LazyFunction(lambda: random.random() * 10)
    publication_date = Faker("date_object")


class IssueFactory(DjangoModelFactory):
    class Meta:
        model = "vulnerabilities.Issue"

    vulnerability = SubFactory(VulnerabilityFactory)
    hostname = Faker("name")
    ip_address = Faker("color_name")
    created_at = Faker("date_object")
    fix_date = None
