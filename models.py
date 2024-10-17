from mongoengine import Document, EmailField, connect
from mongoengine.fields import StringField, BooleanField

connect(db="email_contacts", host="localhost", port=27017)

class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True)
    is_sent = BooleanField(default=False)