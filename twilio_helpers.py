from secrets import SID, AUTH
from twilio.rest import Client

POVERTY_STOPLIGHT_WHATSAPP_NUMBER = "whatsapp:+5521933007184"
TEST_NUMBERS = ["+16265887741", "+41786914152"]
EMPANADA_IMG = "https://capitalcommentary.org/wp-content/uploads/2018/01/America%E2%80%99s-Iconic-Food-Items.jpg"

client = Client(SID, AUTH)

# assuming that the whatsapp window is open
def send_messages():
    for number in TEST_NUMBERS:
        message = client.messages.create(
            from_=POVERTY_STOPLIGHT_WHATSAPP_NUMBER,
            media_url=EMPANADA_IMG,
            body="Lunch is ready!",
            to="whatsapp:" + number,
        )

        print(f"{number}, {message.sid}")

    return

def send_template(whatsapp_number):
    message = client.messages.create(
        from_=POVERTY_STOPLIGHT_WHATSAPP_NUMBER,
        body="Hola, esto es Semáforo de eliminación de pobreza. ¿Te gustaría recibir tu mapa de vida?",
        to="whatsapp:" + whatsapp_number,
    )

    print(f"{whatsapp_number}, {message.sid}")

    return