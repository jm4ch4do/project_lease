from faker import Faker
from app_lease.test.utils.random_user import Provider, random_user
from app_lease.models import Lead
from datetime import datetime


def random_lead(total=1, user=None):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # ----- create leads
    created_leads = []
    for _ in range(total):

        # create lead
        created_lead = Lead.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            source=fake.get_random_source(),
            notes=fake.paragraph(nb_sentences=3),
            dob=fake.date_between(start_date=datetime(1950, 1, 1), end_date=datetime(2003, 1, 1)),
        )

        created_leads.append(created_lead)

    if len(created_leads) == 1:
        return created_lead
    else:
        return created_leads
