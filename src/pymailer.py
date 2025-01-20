try:
    from smtplib import SMTP 
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    from imap_tools import MailBox
    from bs4 import BeautifulSoup
except ImportError:
    print("Import Error, try: 'pip install -r requirements.txt' or 'pip install imap_tools==1.9.1, bs4==0.0.2'")
    exit()

class PyMailer:
    """
    Simple class to fetch emails from an IMAP server and send emails via SMTP.
    
    Args:
        username (str): The username to login into IMAP and SMTP servers.
        password (str): The password to login into IMAP and SMTP servers.
        imap_server (str, optional): The IMAP server address. Defaults to 'imap.gmail.com'.
        imap_port (int, optional): The IMAP server port. Defaults to 993.
        smtp_server (str, optional): The SMTP server address. Defaults to 'smtp.gmail.com'.
        smtp_port (int, optional): The SMTP server port. Defaults to 587.
    """
    def __init__(self, username, password, imap_server='imap.gmail.com', imap_port=993, smtp_server='smtp.gmail.com', smtp_port=587):
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
      
    def parse(self, email_content) -> str:
        """Returns str: text from html"""
        return BeautifulSoup(email_content, 'html.parser').get_text()

    def fetch(self, criteria='ALL', charset='US-ASCII', limit=1, mark_seen=True, reverse=True, headers_only=False, bulk=False, sort=None) -> list[dict]:
        """
        Fetch emails from the IMAP server.
        
        Args:
            criteria (str, optional): IMAP search criteria. Defaults to 'ALL'.
            charset (str, optional): Character set for decoding email content. Defaults to 'US-ASCII'.
            limit (int, optional): Maximum number of emails to fetch. Defaults to 1.
            mark_seen (bool, optional): Whether to mark emails as seen after fetching. Defaults to True.
            reverse (bool, optional): Whether to fetch emails in reverse order. Defaults to True.
            headers_only (bool, optional): Whether to fetch only email headers. Defaults to False.
            bulk (bool, optional): Whether to fetch emails in bulk. Defaults to False.
            sort (str, optional): Sorting criteria for fetching emails. Defaults to None.

        Returns:
            list[dict]: List of dictionaries containing email data. 
            Each dictionary contains the following keys:
                - 'uid': Unique identifier of the email.
                - 'subject': Subject of the email.
                - 'from': Sender of the email.
                - 'to': Recipient(s) of the email.
                - 'date': Date of the email.
                - 'text': Text content of the email.
                - 'html': HTML content of the email.
                - 'attachments': List of attachments in the email.
        """
        with MailBox(self.imap_server, self.imap_port).login(self.username, self.password) as mb:
            raw_emails = mb.fetch(
                criteria=criteria,
                charset=charset,
                limit=limit,
                mark_seen=mark_seen,
                reverse=reverse,
                headers_only=headers_only,
                bulk=bulk,
                sort=sort
            )
            emails = []
            for raw_email in raw_emails:
                email_data = {
                    'uid': raw_email.uid,
                    'date': raw_email.date,
                    'from': raw_email.from_,
                    'to': raw_email.to,
                    'subject': raw_email.subject,
                    'text': '',
                    'html': '',
                    'attachments': []
                }
                
                if raw_email.html:
                    email_data['html'] = raw_email.html
                    email_data['text'] = self.parse(raw_email.html)
                elif raw_email.text:
                    email_data['text'] = self.parse(raw_email.text)
                else:
                    email_data['text'] = ''

                if raw_email.attachments:
                    email_data['attachments'] = [
                        {'filename': att.filename, 'content': att.payload} 
                        for att in raw_email.attachments
                    ]
                emails.append(email_data)
        return emails

    def send(self, to, subject='', body='', html='', attachments=[]) -> str:
        """
        Send a email using the SMTP server. 
        
        Args:
            to (str): Recipient email address.
            subject (str, optional): Email subject. Defaults to empty string.
            body (str, optional): Email body. Defaults to empty string.
            html (str, optional): HTML content structure. Defaults to empty string.
            attachments (list, optional): List of attachment(s). Defaults to empty list.
        
        Returns:
            str: Response from the SMTP server.
        """
        try:
            message = MIMEMultipart()
            message["From"] = self.username
            message["To"] = to
            message["Subject"] = subject

            if body:
                message.attach(MIMEText(body, "plain"))
            if html:
                message.attach(MIMEText(html, "html"))

            if attachments:
                for file_path in attachments:
                    try:
                        with open(file_path, "rb") as file:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(file.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename={file_path.split('/')[-1]}"
                        )
                        message.attach(part)
                    except Exception as e:
                        print(f"Failed to attach file {file_path}: {e}")

            with SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  
                server.login(self.username, self.password)  
                server.send_message(message)  
                return "200 OK"

        except Exception as e:
            return f"Failed to send email: {e}"