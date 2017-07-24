from datetime import datetime


class Word(object):
    '''
    Represents a word object with its text and the timestamp it was created
    '''
    def __init__(self, text):
        self.text = text
        self.timestamp = datetime.now()