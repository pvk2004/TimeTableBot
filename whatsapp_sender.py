from twilio.rest import Client

def send_whatsapp_message_twilio(account_sid, auth_token, from_whatsapp_number, to_whatsapp_number, message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
    print(f"Message sent! SID: {message.sid}")
