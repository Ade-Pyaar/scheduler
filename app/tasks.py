from celery import shared_task

from .models import MyUsers
from app.pdf.main import get_report
from app.my_email import send_my_email

from datetime import datetime
import os

today_date = datetime.today()


# sauce code: 74917


@shared_task
def send_mail_task():
    print("Sending emails")
    final = ""
    
    users = MyUsers.objects.all()

    for user in users:

        if user.email_service:

            user_listing = user.email_listing.get("emails", None)

            if user_listing is not None:

                file_name = f"Report for {user.username} for {today_date.strftime('%m - %Y')}.pdf"

                body = """
                Attached to this email is the monthly report from a website.
                
                Thanks.
                """

                # use the user object to extract the necessary data from the database to form the pdf report
                get_report(file_name) #this method will create the pdf and save it.

                for single_mail in user_listing:
                    send_my_email(single_mail, body, file_name)
# sauce code: 219358
                
                final += f"All email sent for {user.username}"
                os.remove(file_name)
    
    print(final)
