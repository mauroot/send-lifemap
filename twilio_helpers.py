
# from secrets import SID, AUTH
import os
from twilio.rest import Client
from connect_database import connect_mongo
# from app import pdfnetor

SID = os.getenv("SID")
AUTH = os.getenv("AUTH")
BASE_URL = os.getenv("BASE_URL")
URL = f"{BASE_URL}static/pdf/"

if not SID or not AUTH:
    raise Exception(
        """SID or AUTH environmental variables are not configured
        configure an .env file or execute
        export SID="<SIDinfo>"
        export AUTH="<AUTHinfo>"
        Get this info from https://www.twilio.com/console"""
    )

POVERTY_STOPLIGHT_WHATSAPP_NUMBER = "whatsapp:+5521933007184"
TEST_NUMBERS = ["+595981583725"]#,"+16265887741", "+41786914152"]
EMPANADA_IMG = "https://capitalcommentary.org/wp-content/uploads/2018/01/America%E2%80%99s-Iconic-Food-Items.jpg"
LIFEMAP_IMG = "https://bisque-cassowary-8423.twil.io/assets/lifemap-final.jpg"
client = Client(SID, AUTH)

# assuming that the whatsapp window is open
def send_messages(indicator, form_message):
    db = connect_mongo()
    numbers = db["numbers"] # collection should only contain a list objects, with nmuber filed
    # exclude _id Mongo's ObjectID field for correct jsonification
    whatsapp_numbers = list(numbers.distinct("number"))
    print(whatsapp_numbers)
    for number in whatsapp_numbers:
    # for numberObj in TEST_NUMBERS:
        number=str(number)
        print(number)
        try:
            message = client.messages.create(
                from_ = POVERTY_STOPLIGHT_WHATSAPP_NUMBER,
                media_url = EMPANADA_IMG,
                body = "You recevied this message because you have a red " + str(indicator) + " \n" + str(form_message),
                to = number,
            )

        except Exception as e:
            print(e)
            print("phone probably not existent")
        finally:
            print(number, message.sid)
    return

def send_template(whatsapp_number):
    message = client.messages.create(
        from_ = POVERTY_STOPLIGHT_WHATSAPP_NUMBER,
        media_url = LIFEMAP_IMG,
        body = "Hello, this is Poverty Stoplight. Here is your lifemap.",
        to = whatsapp_number,
    )

    print("{}, {}".format(whatsapp_number, message.sid))

    return

def send_pdf(whatsapp_number):
    #pdfnetor(whatsapp_number)
    message = client.messages.create(
        from_ = POVERTY_STOPLIGHT_WHATSAPP_NUMBER,
        media_url = f"http://{BASE_URL}static/pdf/{whatsapp_number}.pdf",
        body = "Hola! Este es tu Mapa de vida",
        to = whatsapp_number,
    )

    print("{}, {}".format(whatsapp_number, message.sid))

    return
