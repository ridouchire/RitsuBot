class Message:
    def __init__(self, text):
        self.text = text
        
    def getType(self):
        return 'groupchat'

    def getBody(self):
        return self.text

class Bot:
    self_nick = {}
    def __init__(self, room, nick):
        self.self_nick[room] = nick
    def send_room_message(self, target, res):
        print('target: {}, message: {}\n'.format(target, res))
    
room = 'ume@conference.ume.mooo.com'
nick = 'test'
