def send_sms(message):
    try:
        from twilio.rest import Client
        # TODO: Replace with your real Twilio credentials and phone numbers
        account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
        auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
        from_number = '+1234567890'
        to_number = '+0987654321'
        client = Client(account_sid, auth_token)
        client.messages.create(body=message, from_=from_number, to=to_number)
        print(f"Twilio SMS sent: {message}")
    except ImportError:
        print(f"[MOCK] Sending SMS: {message}")
    except Exception as e:
        print(f"Twilio SMS failed: {e}")
