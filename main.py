import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from classifier import predict_phishing




# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]


def validator():
    """
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
            )
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def get_unread_emails():
    
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=validator())
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
        messages = results.get('messages', [])
        emails = []
        # if not messages:
        #     print('there are no unread messages ')
        #     return
        
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = msg_data['payload']
            body = ""

            if 'parts' in payload:
                for part in payload['parts']:
                    if part.get('mimeType') == 'text/plain':  # Extract plain text content
                        body = part['body'].get('data', '')
                        break
            else: 
                body = payload.get('body', {}).get('data', '')

            if body:
                body_text = base64.urlsafe_b64decode(body).decode('utf-8', errors='ignore')
                emails.append((msg['id'], body_text.strip('\r\n')))
        
        return emails
    
        # return emails
        
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
        return None


def apply_phishing_prediction_labels(msg_id, msg_label_id):
    service = build("gmail", "v1", credentials=validator())
    # service.users().messages().modify(userId='me', id=msg_id, body={"addLabelIds": ["SPAM"], "removeLabelIds": ["INBOX"]}).execute()
    try:
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={"addLabelIds": [msg_label_id]}
        ).execute()
        print(f"Applied label ID '{msg_label_id}' to email {msg_id}.")
    except HttpError as error:
        print(f"Failed to apply label to email {msg_id}: {error}")

def create_label(label_text):
    service = build("gmail", "v1", credentials=validator())
    """Creates a new label in the Gmail account."""
    existing_labels = {}
    # Call the Gmail API to get labels
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
        print("No labels found")
    else:
        for label in labels:
            existing_labels[label["name"]] = label["id"]

    if label_text in existing_labels:
        return existing_labels[label_text]
    label_body = {
        "name": label_text,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show"
    }

    try:
        if label_text not in existing_labels:
            new_label = service.users().labels().create(userId="me", body=label_body).execute()
            print(f"Label '{new_label['name']}' created successfully with ID: {new_label['id']}.")
            return new_label["id"]
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None



def handle_phishing_detection():
    # 1. Get the messages
    unread_messages = get_unread_emails()
    if not unread_messages:
        print("no unread messages found")
        return
    msg_ids, messages = zip(*unread_messages)
    # Split the list of tuples into two seperate lists with one containing the ids and other containing the messages
    # 2. predict if the message is phishing from the trained model
    predicted_phishing_labels = predict_phishing(messages)
    # 3. create the label => create_label(label)
    created_label_ids = [create_label(label) for label in predicted_phishing_labels]
    # 4. Apply the label
    for msg_id, msg_label_id in zip(msg_ids, created_label_ids):
        apply_phishing_prediction_labels(msg_id, msg_label_id)
    
    

def main():
    handle_phishing_detection()
    

    

if __name__ == "__main__":
  main()