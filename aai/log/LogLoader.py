from aai.log.LogObserver import LogObserver
from aai.log.UserLog import UserLog


class LogLoader(LogObserver):
    logs = {}
    observers = []

    def __init__(self):
        print("loader initialized")
        return

    def get_log(self, id):
        log = self.logs.get(id)
        if not log:
            log = UserLog(id)
            for delay, observer in self.observers:
                log.register(delay, observer)
            self.logs[id] = log

        return log

    def register(self, delay, observer):
        self.observers.append({delay, observer})
