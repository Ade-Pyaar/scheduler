from django.http import HttpResponse
from datetime import datetime
from decouple import Config

from .models import MyUsers

from mailjet_rest import Client
from app.pdf.main import get_report

import base64, os


today_date = datetime.today()


def home(request):
    return HttpResponse("Hello World")



def subscribe(request):
    api_key = "21d45ca21209c2eb50bba6ca121c3be3"
    api_secret = "46fd08c7187ae0829b1b244fd703f166"
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    
    users = MyUsers.objects.all()

    for user in users:

        if user.email_service:

            user_listing = user.email_listing.get("emails", None)
            if user_listing is not None:

                file_name = f"Report for {user.username} for {today_date.strftime('%m - %Y')}.pdf"

                # use the user object to extract the necessary data from the database to form the pdf report
                get_report(file_name) #this method will create the pdf and save it.
                recipient = [  {
                        "Email": entry,
                        "Name": entry
                        } for entry in user_listing
                ]
                
                # get the base64 encoding of the pdf file content
                # try:
                with open(file_name, "rb") as pdf_file:
                    encoded_string = base64.encodebytes(pdf_file.read())
                    final_string = encoded_string.decode('ascii')
                # except Exception as e:
                    # print(str(e))

                data = {
                    'Messages': [
                        {
                        "From": {
                                "Email": "adebayocsc172145@futa.edu.ng",
                                "Name": "Ibrahim Adebayo"
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

                if result.status_code == '200' or result.status_code == 200:
                    os.remove(file_name)
                    return HttpResponse(f"Email sent for {user.username}")
                else:
                    os.remove(file_name)
                    return HttpResponse(f"Email not sent for {user.username}")



    