import os
import json
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client


# LOAD ENV
load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
PHONE_FROM = os.getenv("TWILIO_PHONE_FROM")

print("ACCOUNT_SID:", ACCOUNT_SID)
print("AUTH_TOKEN:", AUTH_TOKEN)
print("WHATSAPP_FROM:", WHATSAPP_FROM)
print("PHONE_FROM:", PHONE_FROM)

if not ACCOUNT_SID or not AUTH_TOKEN:
    raise ValueError("Twilio credentials not found in .env file")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

CONTACTS_FILE = "contacts.json"
LOG_FILE = "message_log.json"


def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_log(entry):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except:
                logs = []

    logs.append(entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)

def log_action(action_type, recipient, status, details=""):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action_type,
        "recipient": recipient,
        "status": status,
        "details": details
    }
    save_log(entry)


# WHATSAPP MESSAGE
def send_whatsapp_message(recipient_number, message_body):
    try:
        message = client.messages.create(
            from_=WHATSAPP_FROM,
            body=message_body,
            to=f"whatsapp:{recipient_number}"
        )
        print(f"WhatsApp sent to {recipient_number} | SID: {message.sid}")
        log_action("whatsapp", recipient_number, "success", message.sid)
    except Exception as e:
        print(f"Failed to send WhatsApp to {recipient_number}: {e}")
        log_action("whatsapp", recipient_number, "failed", str(e))


# BULK WHATSAPP
def send_bulk_whatsapp(message_body):
    contacts = load_contacts()
    if not contacts:
        print("No contacts found.")
        return

    for contact in contacts:
        name = contact.get("name", "User")
        phone = contact.get("phone")
        if phone:
            msg = message_body.replace("{name}", name)
            send_whatsapp_message(phone, msg)


# VOICE CALL
def make_voice_call(recipient_number, text):
    try:
        call = client.calls.create(
            twiml=f'<Response><Say>{text}</Say></Response>',
            to=recipient_number,
            from_=PHONE_FROM
        )
        print(f"Call placed to {recipient_number} | SID: {call.sid}")
        log_action("call", recipient_number, "success", call.sid)
    except Exception as e:
        print(f"Call failed: {e}")
        log_action("call", recipient_number, "failed", str(e))


# BULK CALL
def make_bulk_calls(text):
    contacts = load_contacts()
    for contact in contacts:
        name = contact.get("name", "User")
        phone = contact.get("phone")
        if phone:
            msg = text.replace("{name}", name)
            make_voice_call(phone, msg)


# TEMPLATES
TEMPLATES = {
    "reminder": "Hello {name}, this is your reminder.",
    "menu": "Hi {name}, welcome!\n1. Menu\n2. Order\n3. Support"
}

# MENU
def show_menu():
    print("\n===== MENU =====")
    print("1. Send WhatsApp (single)")
    print("2. Send WhatsApp (bulk)")
    print("3. Schedule reminder")
    print("4. Call one person")
    print("5. Call all contacts")
    print("6. Show contacts")
    print("7. Run scheduler")
    print("8. Exit")

def show_contacts():
    contacts = load_contacts()
    for c in contacts:
        print(c["name"], "-", c["phone"])


def main():
    while True:
        show_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            num = input("Enter number (+91...): ")
            msg = input("Enter message: ")
            send_whatsapp_message(num, msg)

        elif choice == "2":
            msg = input("Enter message (use {name}): ")
            send_bulk_whatsapp(msg)

        elif choice == "3":
            t = input("Enter time (HH:MM): ")
            schedule.every().day.at(t).do(send_bulk_whatsapp, TEMPLATES["reminder"])
            print("Scheduled!")

        elif choice == "4":
            num = input("Enter number: ")
            text = input("Enter call text: ")
            make_voice_call(num, text)

        elif choice == "5":
            text = input("Enter call text: ")
            make_bulk_calls(text)

        elif choice == "6":
            show_contacts()

        elif choice == "7":
            print("Scheduler running...")
            while True:
                schedule.run_pending()
                time.sleep(1)

        elif choice == "8":
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()