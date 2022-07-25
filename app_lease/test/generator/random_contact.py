from faker import Faker
from app_lease.test.generator.random_customer import random_customer
from app_lease.test.generator.random_lead import random_lead
from app_lease.utils.fake_provider import Provider
from app_lease.models import Contact


def random_contact(total=1, related_to='customer', contact_type=1, user=None):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    created_contacts = []
    for _ in range(total):

        # create customer or lead
        created_customer, created_lead = None, None
        if related_to == 'customer':
            created_customer = random_customer()
        elif related_to == 'lead':
            created_lead = random_lead()

        # create phone or email
        phone, email = None, None
        if contact_type == 1 and related_to == 'customer':
            email = created_customer.user.email
        elif contact_type == 1 and related_to == 'lead':
            random_user_name = Provider.get_random_user_name(created_lead.first_name)
            email = random_user_name + "@gmail.com"
        elif contact_type == 2:
            random_phone = int("1" + str(fake.msisdn()[3:]))
            phone = random_phone

        # create contact
        created_contact = Contact.objects.create(
            customer=created_customer,
            lead=created_lead,
            phone=phone,
            email=email,
            note=fake.paragraph(nb_sentences=3),
            type=contact_type,
        )

        created_contacts.append(created_contact)

    if len(created_contacts) == 1:
        return created_contact
    else:
        return created_contacts
