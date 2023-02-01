import pickle
import speech_recognition as sr
import pyttsx3
import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build 
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email import errors
from apiclient import errors
import mimetypes
import base64

l = sr.Recognizer()
engine = pyttsx3.init()

def talk(text):
    engine.say(text)
    engine.runAndWait()


# for getting a information from the user

def get_info():
    try:
        with sr.Microphone() as source:
            print('listening...')
            l.adjust_for_ambient_noise(source, duration=0.2)
            print('123')
            voice = l.listen(source, phrase_time_limit=10)
            info = l.recognize_google(voice)
            print(info)
            return info
    except:
        print('Error.........')
        pass


email_list = {'Rahul': 'manmohanrajpal888@gmail.com', 'Ankit': 'manmohanrajpal889@gmail.com',
              'Ashok': 'manmohanrajpal888@gmail.com'}

SCOPES = ['https://mail.google.com/']

# Authentication Function For Gmail API

global msg
creds = None

if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)
	

def choice():
    talk('Do You want send email or Read a new email')

    try:
        with sr.Microphone() as source:
            print('listening...')
            l.adjust_for_ambient_noise(source, duration=0.2)
            voice = l.listen(source, phrase_time_limit=3)
            choice = l.recognize_google(voice)
            print(choice)
            if "send" in choice:
                send_choice()
            if "read" in choice:
                read_choice()
    except:
        print('Error.........')
        pass

def send_choice():
    talk('Do You want send email with attachment or without attachment')

    try:
        with sr.Microphone() as source:
            print('listening...')
            l.adjust_for_ambient_noise(source, duration=0.2)
            voice = l.listen(source, phrase_time_limit=3)
            print('123')
            choice = l.recognize_google(voice)
            print(choice)

            if "without attachment" in choice:
                talk('If you want to send email from existing list then say list or say new for a new user')
                try:
                    with sr.Microphone() as source:
                        print('listening...')
                        l.adjust_for_ambient_noise(source, duration=0.2)
                        voice = l.listen(source, phrase_time_limit=3)
                        choice1 = l.recognize_google(voice)
                        print(choice1)
                        if "list" in choice1:
                            get_emailInfowo()
                        if "new" in choice1:
                            get_emailInfo1wo() #demook812@gmail.com
                except:
                    print('Error.........')
                    pass

            elif "with attachment" in choice:
                talk('If you want to send email from existing list then say list or say new for a new user')
                try:
                    with sr.Microphone() as source:
                        print('listening...')
                        l.adjust_for_ambient_noise(source, duration=0.2)
                        voice = l.listen(source, phrase_time_limit=3)
                        choice2 = l.recognize_google(voice)
                        print(choice)
                        if "list" in choice2:
                            get_emailInfowa()
                        if "new" in choice2:
                            get_emailInfo1wa() #demook812@gmail.com
                except:
                    print('Error.........')
                    pass
    except:
        print('Error in Something')
        talk('Error in Something')
        pass

def get_emailInfowo():
    talk('To whom You Want To Send The Email')
    name = get_info()
    reciever = email_list[name]
    print(reciever)
    talk('What Is The Subject Of Your Email')
    subject = get_info()
    talk('What Is The Message You Want To Send')
    message = get_info()
    send_emailwo(reciever, subject, message)
    print('Email Sent Successfully')
    talk('Email Sent Successfully')

def get_emailInfo1wo():
    talk('Please provide the email id of person to whom you want to send email')
    email_id = get_info()
    if "at the rate " in email_id:
        email_id = email_id.replace("at the rate", "@")
    email_id = email_id.replace(" ", "")
    if 'dot' in email_id:
        email_id = email_id.replace("dot", ".")
    talk('Please check the email id ')
    for i in email_id:
        talk(i)
    talk('Do You want to proceed with this Mail id say okay if email is correct or Not okay for disagree')
    option =get_info()
    if (option == 'okay'):
        print(email_id)
        talk('What Is The Subject Of Your Email')
        subject = get_info()
        talk('What Is The Message You Want To Send')
        message = get_info()
        send_emailwo(email_id, subject, message)
        print('Email Sent Successfully')
        talk('Email Sent Successfully')
    if (option == 'not okay'):
        get_emailInfo1wo()
        talk('Try again')

def send_emailwo(reciever, subject, message):
    gmail_from='demoop84458@gmail.com'
    message = MIMEText(message)
    message['to'] =reciever
    message['from']=gmail_from
    message['subject']=subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw =raw.decode()
    body ={'raw':raw}
    try:
        message = (service.users().messages().send(userId ='me',body =body).execute())
        print("Your message has been sent")
        talk("Your message has been sent")
    except errors.MessageError as error:
        print('An error occurred: %s' %error)
        talk('An error occurred') 

def get_emailInfo1wa():
    talk('Please provide the email id of person to whom you want to send email')
    email_id = get_info()
    if "at the rate " in email_id:
        email_id = email_id.replace("at the rate", "@")
    email_id = email_id.replace(" ", "")
    if 'dot' in email_id:
        email_id = email_id.replace("dot", ".")
    talk('Please check the email id ')
    for i in email_id:
        talk(i)
    talk('Do You want to proceed with this Mail id say okay if email is correct or Not okay for disagree')
    option =get_info()
    if (option == 'okay'):
        print(email_id)
        talk('What Is The Subject Of Your Email')
        subject = get_info()
        talk('What Is The Message You Want To Send')
        message = get_info()
        talk('What is the name of file')
        file_name = get_info().lower()
        if 'dot' in file_name:
            file_name=file_name.replace("dot", ".")
        if ' ' in file_name:
            file_name = file_name.replace(" ", "") 
        send_emailwa(email_id, subject, message ,file_name)
        print('Email Sent Successfully')
        talk('Email Sent Successfully')
    if (option == 'not okay'):
        get_emailInfo1wo()
        talk('Try again')
        

def get_emailInfowa():
    talk('To whom You Want To Send The Email')
    name = get_info()
    reciever = email_list[name]
    print(reciever)
    talk('What Is The Subject Of Your Email')
    subject = get_info()
    talk('What Is The Message You Want To Send')
    message = get_info()
    talk('What is the name of file')
    file_name = get_info().lower()
    send_emailwa(reciever, subject, message ,file_name)
    print('Email Sent Successfully')
    talk('Email Sent Successfully')

def send_messagewa1(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id,
                body=message).execute()

        print('Message Id: {}'.format(message['id']))

        return message
    except Exception as e:
        print('An error occurred: {}'.format(e))
        return None

def create_message_with_attachment(
    sender,
    to,
    subject,
    message_text,
    file,
    ):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    (content_type, encoding) = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'

    (main_type, sub_type) = content_type.split('/', 1)

    if main_type == 'text':
        with open(file, 'rb') as f:
            msg = MIMEText(f.read().decode('utf-8'), _subtype=sub_type)

    elif main_type == 'image':
        with open(file, 'rb') as f:
            msg = MIMEImage(f.read(), _subtype=sub_type)
        
    elif main_type == 'audio':
        with open(file, 'rb') as f:
            msg = MIMEAudio(f.read(), _subtype=sub_type)
        
    else:
        with open(file, 'rb') as f:
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(f.read())

    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment',
                   filename=filename)
    message.attach(msg)

    raw_message = \
        base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
    return {'raw': raw_message.decode('utf-8')}

def send_emailwa(reciever, subject, message,file_name):
    user_id = 'me'
    msg = create_message_with_attachment('demoop84458@gmail.com',reciever, subject,message,file_name)
    send_messagewa1(service, user_id, msg)

def read_choice():
    talk('Do You want read last email or open unread emails ')
    talk('if you want read only last email then talk last or read unread emails then talk unread')
    try:
        with sr.Microphone() as source:
            print('listening...')
            l.adjust_for_ambient_noise(source, duration=0.2)
            voice = l.listen(source, phrase_time_limit=3)
            print('123')
            choice = l.recognize_google(voice)
            print(choice)

            if "last" in choice:
                last_read()
            elif "unread" in choice:
                unread_read()
    except:
        print('Error in Something')
        talk('Error in Something')
        pass

def last_read():
    results = service.users().messages().list(userId='me',labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    message_count = 1
    talk('Last message is ')
    if not messages:
        talk('You have no new messages')
        print('You have no new messages.....')
    else:
        for message in messages[:message_count]:
 
            msg = service.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
 
            for add in msg['payload']['headers']:
                if add['name'] == "From":
 
                    # fetching sender's email name
                    a = str(add['value'].split("<")[0])
                    print(a)
                    talk("email from"+a)
                    print(msg['snippet'])
                    talk(msg['snippet'])

def unread_read():
    results = service.users().messages().list(userId='me',
                                              labelIds=["INBOX", "UNREAD"]).execute()
    # The above code will get emails from primary
    # inbox which are unread
    messages = results.get('messages', [])
 
    if not messages:
 
        # if no new emails
        print('No messages found.')
        talk('No messages found.')
    else:
        talk("{} new emails found".format(len(messages)))
        for message in messages:
 
            msg = service.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
 
            for add in msg['payload']['headers']:
                if add['name'] == "From":
 
                    # fetching sender's email name
                    a = str(add['value'].split("<")[0])
                    print(a)
 
                    talk("email from"+a)
                    print(msg['snippet'])
                    talk(msg['snippet'])
 
            service.users().messages().modify(userId ='me', id = message['id'],body ={'removeLabelIds':['UNREAD']}).execute()
            
choice()


