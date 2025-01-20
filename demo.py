from __init__ import PyMailer 
#from pymailer import PyMailer

mailer = PyMailer(
    username='you@gmail.com',
    password='abcd efgh ijkl mnop',
)

mailer.send(
    to='someone@domain.com',
    subject='Hello',
    body='Hello, World!',
    html='<h1>Hello, World!</h1>',
    attachments=['/path/to/file.pdf', '/path/to/file.png'],
)

email = mailer.fetch()
print(f'UID: {email["uid"]}')
print(f'FROM: {email["from"]}')
print(f'SUBJECT: {email["subject"]}')
print(f'BODY: {email["text"]}')
print(f'HTML: {email["html"]}')
print(f'ATTACHMENTS: {email["attachments"]}')