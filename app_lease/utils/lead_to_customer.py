from datetime import date
from random import randint


def age_from_dob(lead, user_name=None, password=None):
    """
    Turns a lead into a customer and saves in the db. Returns the new customer object
    (lead_object, string, string) -> customer_object
    """

    if not user_name:
        user_name = lead.first_name.lower() + str(randint(1, 999999))

    if not password:
        password = 'Teclado123'

    # create lead
    created_lead = Lead.objects.create(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        source=fake.get_random_source(),
        notes=fake.paragraph(nb_sentences=3),
        dob=fake.date_between(start_date=datetime(1950, 1, 1), end_date=datetime(2003, 1, 1)),
    )

    created_customer = Customer.objects.create(
        user=created_user,
        first_name=created_user.first_name,
        last_name=created_user.last_name,
        job=fake.job(),
        notes=fake.paragraph(nb_sentences=3),
        dob=fake.date_between(start_date=datetime(1950, 1, 1), end_date=datetime(2003, 1, 1)),
        status=Provider.get_customer_status(created_user)  # status matches the user status
    )

    # find years_passed since dob
    today = date.today()
    diff_in_years = today.year - dob.year

    # find if birthday already passed the current year
    if today.month < dob.month:
        has_birthday_passed = False
    elif today.month > dob.month:
        has_birthday_passed = True
    elif today.day >= dob.day:
        has_birthday_passed = True
    else:
        has_birthday_passed = False

    # decide if age is years_passed or years_passed+1
    age = diff_in_years if has_birthday_passed else diff_in_years - 1

    return age
