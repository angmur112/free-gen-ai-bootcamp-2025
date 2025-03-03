from comps import ServiceOrchestrator

class Chat:
    def __init__(self):
        print('init')
        self.megaservice = ServiceOrchestrator()
        self.endpoint = '/angelo chatbot'
    def add_remote_service(self):
        print('add_remote_service')
    def start(self):
         print('start')
    
    if __name__ == '__main__':
        print('main')
        chat = Chat()
        chat.add_remote_service()
        chat.start()
