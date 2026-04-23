import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time

sender = "your_email@gmail.com"
password = "your_app_password"

people = [
    {"name": "Person1", "email": "person1@gmail.com", "dob": "21-04", "hour": 0, "minute": 17},
    {"name": "Person2", "email": "person2@gmail.com", "dob": "21-04", "hour": 0, "minute": 17},
    {"name": "Person3", "email": "person3@gmail.com", "dob": "21-04", "hour": 0, "minute": 17}
]
# Each person has name, email, birthday, and sending time

sent_today = []
# This list stores the emails that already got the birthday message today

print("Waiting for the correct date and time...")

while True:
    now = datetime.now()
    today = now.strftime("%d-%m")

    for person in people:
        # Check each person one by one

        if (
            person["dob"] == today
            and now.hour == person["hour"]
            and now.minute >= person["minute"]
            and person["email"] not in sent_today
        ):
            # Send email only if birthday matches, time matches,
            # and email has not already been sent today

            msg = MIMEText(
                f"Happy Birthday, {person['name']}! 🎉🎂\n"
                f"Wishing you a fantastic day filled with joy and surprises! 🥳🎁\n"
            )
            # Create the email body

            msg["Subject"] = "🎂 Happy Birthday! 🎂"
            # Set email subject

            msg["From"] = sender
            # Set sender email

            msg["To"] = person["email"]
            # Set receiver email

            server = None

            try:
                server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                # Connect securely to Gmail SMTP server

                server.login(sender, password)
                # Login using sender email and app password

                server.send_message(msg)
                # Send the email

                print(f"Email sent successfully to {person['name']} at {person['hour']}:{person['minute']:02d}")
                sent_today.append(person["email"])
                # Save email so it is not sent again today

            except Exception as e:
                print(f"Failed to send email to {person['name']}: {e}")
                # Show error message if email sending fails

            finally:
                if server:
                    server.quit()
                    # Close the server connection safely

    time.sleep(30)
    # Wait for 30 seconds before checking again
