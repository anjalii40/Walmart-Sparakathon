def send_whatsapp(message):
    try:
        from twilio.rest import Client
        # TODO: Replace with your real Twilio credentials and WhatsApp numbers
        account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
        auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
        from_whatsapp = 'whatsapp:+1234567890'
        to_whatsapp = 'whatsapp:+0987654321'
        client = Client(account_sid, auth_token)
        client.messages.create(body=message, from_=from_whatsapp, to=to_whatsapp)
        print(f"Twilio WhatsApp sent: {message}")
    except ImportError:
        print(f"[MOCK] Sending WhatsApp message: {message}")
    except Exception as e:
        print(f"Twilio WhatsApp failed: {e}")
