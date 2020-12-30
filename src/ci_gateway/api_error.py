

class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, verb, url, status):
        self.verb = verb
        self.url = url
        self.status = status

    def __str__(self):
        return f'APIError: {self.verb} {self.url} {self.status}'
