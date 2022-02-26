from celery import shared_task
from mailjet_rest import Client
from django.shortcuts import HttpResponse

from .models import MyUsers
from app.pdf.main import get_report

from datetime import datetime
import base64, os
from decouple import Config

today_date = datetime.today()



@shared_task
def send_mail_task():
        
    api_key = Config("api_key")
    api_secret = Config("api_secret")
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    
    users = MyUsers.objects.all()

    for user in users:

        if user.email_service:

            user_listing = user.email_listing.get("emails", None)
            if user_listing is not None:

                file_name = f"Report for {user.username} for {today_date.strftime('%m - %Y')}"

                # use the user object to extract the necessary data from the database to form the pdf report
                get_report(file_name) #this method will create the pdf and save it.
                recipient = [  {
                        "Email": entry,
                        "Name": entry
                        } for entry in user_listing
                ]
                
                # get the base64 encoding of the pdf file content
                with open(file_name, "rb") as pdf_file:
                    encoded_string = base64.encodebytes(pdf_file.read())
                    final_string = encoded_string.decode('ascii')

                data = {
                    'Messages': [
                        {
                        "From": {
                                "Email": f"{user.email}",
                                "Name": f"{user.username}"
                            },

                        "To": recipient,

                        "Subject": "Monthly report",

                        "TextPart": "You are getting this email because you subscribed for the monthly email service \
                                    Attached to this email is your monthly report.",

                        "HTMLPart": "<h3>Dear passenger 1, welcome to <a href=\"https://www.mailjet.com/\">Mailjet</a>!</h3><br />May the delivery force be with you!",

                        "CustomID": f"Monthly-report for {user.username}",

                        "Attachments": [{"ContentType": "application/pdf",
                                        "Filename": file_name,
                                        "Base64Content": final_string}]
                        }
                    ]
                }

                result = mailjet.send.create(data=data)
                
                print(result.status_code)
                print(result.json())

                if result.staus_code == '200' or result.status_code == 200:
                    os.remove(file_name)



            
                print(f"Email sent for {user.username}")