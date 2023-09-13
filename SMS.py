import smtplib
import os

from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

class SMS:
    
    CARRIERS = {
        'att':    '@mms.att.net',
        'tmobile': '@tmomail.net',
        'verizon':  '@vtext.com',
        'sprint':   '@page.nextel.com'
    }

    # Set the gmail api username and password as environment variables for secrecy
    AUTH_EMAIL = os.environ.get('GMAIL_UN')
    AUTH_PASS = os.environ.get('GMAIL_PWD')

    def __init__(self, to, frm=None, carrier='tmobile'):
        print(SMS.AUTH_EMAIL, SMS.AUTH_PASS)

        self.carrier = carrier if type(carrier) == list else [carrier]
        print(type(to))
        self.to = to if type(to) == list else [to]
        self.to = ['{}{}'.format(self.to[t].strip().replace("-",""), SMS.CARRIERS[self.carrier[t]]) for t in range(len(self.to))]
        self.frm = frm if frm is not None else SMS.AUTH_EMAIL

    def send(self, msg, subj):
        # Establish a secure session with gmail's outgoing SMTP server using your gmail account
        server = smtplib.SMTP( "smtp.gmail.com", 587 )
        # server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(SMS.AUTH_EMAIL, SMS.AUTH_PASS)

        # Send text message through SMS gateway of destination number
        print("Msg: {} to: {}".format(msg, self.to))

        message = MIMEMultipart()
        message["Subject"] = subj
        message["From"] = self.frm
        message["To"] = ", ".join(self.to)
        # message["Cc"] = ", ".join(cc_email)

        msg_txt = MIMEText(msg, "html", 'latin1')
        message.attach(msg_txt)

        # receiver_email = [receiver_email] + cc_email


        server.sendmail(SMS.AUTH_EMAIL, self.to, message.as_string())        


if __name__ == '__main__':

    # Test it out
    msg = 'Hello world.  I am a test message.'

    from SMS import SMS


    sms = SMS('<your phone #>')

    test_html = """\
        <html>
            <body>
                <p>Hello world HTML test.<br></p>
            </body>
        </html>
        """
    
    # sms.send(msg, 'vegas trip')

    # sms.send(test_html, 'test html')

    # Test multiple receivers
    sms_multiple = SMS(['<your phone #>', 'your phone #', 'your phone #'], carrier=['tmobile', 'tmobile', 'tmobile'])
    # sms_multiple.send(test_html, 'vegas trip')

    test_html = """\
        <html>
            <body>
                <p>I am a robot.<br>
                Beep boop <br>
                I poke you.<br></p>
            </body>
        </html>
        """
    
    sms.send(test_html, 'Beep boop')
