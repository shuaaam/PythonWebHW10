from mongoengine import DoesNotExist, MultipleObjectsReturned
from mongoengine.queryset.visitor import Q
from models import Contact


class ExceptError:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, *args):
        try:
            return self.func(*args)
        except DoesNotExist as err:
            print(err)
        except MultipleObjectsReturned as err:
            print('Multiple results found, please be more specific')
        except Exception as err:
            print(err)


@ExceptError
def create_contact(name, last_name, phone):
    Contact(name=name, last_name=last_name, phone=phone).save()


@ExceptError
def change_number(name, last_name, new_phone):
    contact = Contact.objects(Q(name=name) & Q(last_name=last_name))
    contact.update(phone=new_phone)


@ExceptError
def update_email(name, last_name, email):
    contact = Contact.objects(Q(name=name) & Q(last_name=last_name))
    contact.update(email=email)


@ExceptError
def update_last_name(name, last_name):
    contact = Contact.objects(Q(name=name) & Q(last_name=last_name))
    contact.update(last_name=last_name)


@ExceptError
def update_birthday(name, last_name, birthday):
    contact = Contact.objects(Q(name=name) & Q(last_name=last_name))
    contact.update(birthday=birthday)


@ExceptError
def delete_number(name, last_name):
    contact = Contact.objects(Q(name=name) & Q(last_name=last_name))
    contact.update(phone='N/A')


@ExceptError
def remove_contact(name, last_name):
    contact = Contact.objects(Q(name=name) & Q(last_name=last_name))
    contact.delete()


@ExceptError
def delete_all():
    Contact.objects.delete()


@ExceptError
def show_number(name, last_name):
    contact = Contact.objects.get(Q(name=name) & Q(last_name=last_name))
    phone = contact.phone
    return phone


@ExceptError
def show_all():
    numbers = Contact.objects.count()
    for c in Contact.objects:
        print(
            f'Name: {c.name} \n'
            f'Last name: {c.last_name} \n'
            f'Phone: {c.phone}\n'
            f'Email: {c.email}\n'
            f'Birthday: {c.birthday}\n')
    return numbers


@ExceptError
def show_birthday(name, last_name):
    contact = Contact.objects.get(Q(name=name) & Q(last_name=last_name))
    birthday = contact.birthday
    return birthday


@ExceptError
def find(sub):
    user = Contact.objects.search_text(sub).first()
    if user:
        return f'Name {user.name},\n' \
               f'Last name {user.last_name},\n' \
               f'Phone: {user.phone},\n' \
               f'Birthday: {user.birthday},\n' \
               f'Email: {user.email},\n'
    else:
        return f'No information found for {sub}'
