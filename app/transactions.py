import uuid
from app.models.lamportclock import Vector_Clock


class Transaction:
    def __init__(self, clock: Vector_Clock, value, pix_key):
        self.id = uuid.uuid4()
        self.type = 0
        self.clock = clock
        self.__value = value
        self.__pix_key = pix_key
        self.status = 0

        @property  # rever isso
        def value():
            return self.__value

        def _status_change(self, status):
            self.status = status

        def _transaction_kill(self):
            del self
