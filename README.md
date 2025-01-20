
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
2. Install dependencies:

pip install -r requirements.txt

## Usage


from pymailer import PyMailer

mailer = PyMailer()
mailer.send_email(
    to="recipient@domain.com",
    subject="Test Email",
    body="Hello from PyMailer!",
    attachments=["path/to/file.pdf"]
)
Note: As of now you can only sign in with gmail

## Security Note

- Use App Passwords for Gmail instead of your account password
- Keep your credentials secure

## License

MIT License
