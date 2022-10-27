from mongoengine import *

connect(host='mongodb://localhost:27017/contactbook')


class Contact(Document):
    name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50, required=True)
    phone = StringField(max_length=20, required=True)
    email = EmailField()
    birthday = DateField()


