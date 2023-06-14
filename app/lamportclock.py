import config as conf


class Vector_Clock:
    def __init__(self, peer_number=int(conf.PROCESSES_QUANTITY)):
        self.peer_number = peer_number
        self.clock = [0 for i in range(self.peer_number)]

    # IDEIA: Usar funcão @app.before_request
    def update(self, sClock):
        for i in range(self.peer_number):
            self.clock[i] = max(self.clock[i], sClock[i])

        self.event()

    def event(self):
        self.clock[int(self.id)] = self.clock[int(self.id)] + 1

    def __repr__(self):
        return f'"peer_number": {self.peer_number},"clock": {self.clock}'
