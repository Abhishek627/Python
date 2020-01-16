import imaplib
import email
import PyPDF2

def read_email_from_gmail():
    '''
    Provide user and email in below variables.
    select label to search
    And then save it to some location
    :return:
    '''
    USER= "user@gmail.com"
    PASSWORD = "user-password"
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(USER,PASSWORD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    email_subject = msg['subject']
                    data= get_body(msg)
                    save_pdf(email_subject,data)
    except Exception, e:
        print e

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

def save_pdf(topic, msg):
    file_name = "downloads/"+topic+".html"
    with open(file_name,"w+") as path:
        path.write(msg)
        print "written to file", file_name

read_email_from_gmail()