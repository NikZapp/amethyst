import queue
from connection import Connection

class Chat:
    def __init__(self, log):
        self.log = log
        self.messages = queue.Queue()
        log_file = open(log, 'r')
        self.parsed = len(log_file.readlines())
        log_file.close()

    def get_messages(self):
        self.messages = queue.Queue()
        log_file = open(self.log, 'r')
        lines = log_file.readlines()
        log_file.close()
    
        # Queue found messages
        if len(lines) - self.parsed > 0: # If there are new lines
            for line in lines[-(len(lines) - self.parsed):]:
                self.messages.put(line[:-1])
            self.parsed = len(lines)
    
    def send(self, message):
        connection = Connection("localhost", 4711)
        connection.send(b"chat.post", message)
        connection.close()

