import xmpp

def connect_jabber():
    client = xmpp.Client(JABBER_SERVER)
    client.connect(server=(JABBER_SERVER, JABBER_PORT))
    client.auth(JABBER_USER,JABBER_PASS,JABBER_NAME)
    client.sendInitPresence()
    client.send(xmpp.Presence(to="%s/%s" % (JABBER_ROOM, JABBER_NAME)))
    return client

def send_jabber_message(client, messagebody):
    message = xmpp.protocol.Message(body=messagebody)
    message.setTo(JABBER_ROOM)
    message.setType('groupchat')
    client.send(message)

# Connect to jabber.
jabber_client = connect_jabber()
