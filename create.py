from models import Contact
from time import time
from faker import Faker

fake = Faker('uk_UA')


def create_contacts(count):
    timer = time()
    for _ in range(count):
        Contact(
            name=fake.first_name(),
            last_name=fake.last_name(),
            phone=fake.phone_number(),
            birthday=fake.date_between(start_date='-50y'),
            email=fake.ascii_free_email()).save()

    print(f'{count} contacts created in {round(time() - timer, 3)} seconds')


if __name__ == '__main__':
    create_contacts(50)
