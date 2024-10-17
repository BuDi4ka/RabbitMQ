import pika
from mongoengine import connect
from models import Contact

connect(db="email_contacts", host="localhost", port=27017)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue', durable=True)

def send_email(contact):
    print(f"Надсилаємо email контакту: {contact.fullname} ({contact.email})")
    contact.update(is_sent=True)
    contact.reload()

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.is_sent:
        send_email(contact)
        print(f"Email відправлено для контакту: {contact.fullname}")
    else:
        print(f"Контакт з ID: {contact_id} не знайдено або email вже відправлено")

channel.basic_consume(queue='email_queue',
                      on_message_callback=callback,
                      auto_ack=True)

print('Очікування повідомлень. Натисніть CTRL+C для виходу.')
channel.start_consuming()

