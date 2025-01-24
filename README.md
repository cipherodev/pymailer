
# PyMailer

A simple lightweight program to send and fetches emails using SMTP and IMAP.

## Features

- Send emails using SMTP
- Fetch emails using IMAP 
- Support for HTML content
- Attachment handling

## Requirements

- Python 3.6+

## Setup

1. Clone this repository
```
git clone https://github.com/cipherodev/pymailer.git
```
3. Enter pymailer directory
4. Install dependencies:
```
pip install -r requirements.txt
```
## Usage

```
from pymailer import PyMailer

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

email = mailer.fetch()[0]
print(f'UID: {email["uid"]}')
print(f'FROM: {email["from"]}')
print(f'SUBJECT: {email["subject"]}')
print(f'BODY: {email["text"]}')
print(f'HTML: {email["html"]}')
print(f'ATTACHMENTS: {email["attachments"]}')
```
Note: As of now you can only sign in with gmail

## Tip
For the password use your google app password. To create one go to <a href="https://myaccount.google.com/?tab=kk">Google account page</a> 
Navigate to "apps passwords" and create a new one named "pymailer". Use the password it gives you.

## Security Note

- Use App Passwords for Gmail instead of your account password
- Keep your credentials secure

## License

MIT License
