import pika
import faker
from faker.proxy import Faker
from mongoengine import connect

from models import Contact

connect(db='email_contacts',host='localhost',port=27017)

fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='email_mock')
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_bind(exchange='email_mock', queue='email_queue')


def generate_contacts(num):
    for i in range(num):
        contact = Contact(
            fullname = fake.name(),
            email = fake.email(),
        )
        contact.save()
        channel.basic_publish(exchange='',
                              routing_key='email_queue',
                              body=str(contact.id))

if __name__ == '__main__':
    generate_contacts(20)
    connection.close()
