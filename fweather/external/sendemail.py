import httplib2
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
from oauth2client import file, client, tools
import asyncio
import time
import os
import tempfile


class Gmail(object):
    """Simple class to send emails using the gmail api.

    Modified from https://stackoverflow.com/a/37267330/2965993

    This should be its own package on pip. :)
    """

    SCOPES = 'https://www.googleapis.com/auth/gmail.send'
    # location of cached token file after allowing connection
    GMAIL_TOKEN_FILE = 'credentials.json'
    APPLICATION_NAME = 'Gmail API Python Send Email'

    def __init__(self):
        """Initialize Gmail by getting creds if they exist or by requesting oauth access."""
        # set and check the store
        store = file.Storage(os.path.join(os.getcwd(), self.GMAIL_TOKEN_FILE))
        credentials = store.get()
        http = httplib2.Http()
        # write env var to a temporary file, then pass in the secure file to the flow object
        if not credentials or credentials.invalid:
            fd, temp_path = tempfile.mkstemp()
            with open(temp_path, 'w') as fp:
                fp.write(os.getenv('gmail'))
            flow = client.flow_from_clientsecrets(temp_path, scope=self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            # close temp file descriptor to prevent memory leaks
            # source: https://www.logilab.org/blogentry/17873
            os.close(fd)
            credentials = tools.run_flow(flow, store, http=http)
        http = credentials.authorize(http)
        self.service = discovery.build('gmail', 'v1', http=http)

    def create_message(self, to, subject, body):
        """Create an HTML message containing the correct headers.

        :param to: address to send an email to
        :param subject: subject of the message
        :param body: body of the message
        :return: base64 encoded msg attributes
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        # msg['From'] = self.sender
        msg['To'] = to
        msg.attach(MIMEText(body, 'html'))
        return {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}

    def send(self, to, subject, body):
        message = self.create_message(to, subject, body)
        try:
            res = (self.service.users().messages().send(userId='me', body=message).execute())
            return res
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    async def asend(self, to, subject, body):
        """Sends the email asynchronously

        :param to: address to send an email to
        :param subject: subject of the message
        :param body: body of the message
        :return: response from gmail
        """
        return self.send(to, subject, body)


if __name__ == '__main__':
    # important vars
    receive_email = os.getenv('test_email')
    subj = 'Subject matter #{}'
    msg_body = 'Your <strong>body</strong> is a temple'

    gmail = Gmail()
    
    start = time.time()

    loop = asyncio.get_event_loop()
    tasks = [
        gmail.asend(receive_email, subj.format(i), msg_body)
        for i in range(1)
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    print('Total time: {}'.format(time.time() - start))
