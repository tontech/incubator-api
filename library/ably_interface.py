from ably import AblyRest

class AblyInterface:

    def __init__(self):
        self.client = AblyRest('tsKhkA.cQNtHQ:8vT9W-JS33QfCxfY')
        self.channel = self.client.channels.get('test')
        self.event = 'ho-m2a-68617463686f636c6f636b'
        self.push_event = 'ho-notif-68617463686f636c6f636b'

    def publish_message(self, message):
        self.channel.publish(self.event,message)

    def push_notif(self, message):
        self.channel.publish(self.push_event,message)
        

