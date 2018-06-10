import time

logs = {}
observers = []


def get_log(self, id):
    self.count = self.count + 1
    print("get from loader, count" + str(self.count))
    log = self.logs.get(id)
    if not log:
        log = UserLog(id)
        self.logs[id] = log
    return log


class UserLog:
    logs = {}
    observers = []
    id = ""
    count = 0
    LOG_TYPE_SEARCH = "SEARCH"

    def __init__(self, id):
        self.id = id
        self.logs = {}

    def get_logs(self):
        self.count = self.count + 1
        return self.logs

    def add_search(self, argument):
        self.count = self.count + 1
        self.logs[time.time()] = {"VALUE": argument, "TYPE": self.LOG_TYPE_SEARCH}
        print("log for " + self.id)
        logs = self.logs
        for delay, observer in self.observers:
            observer.on_log(self.id, logs)

    def get_id(self):
        return self.id

    # delay in seconds, zero for infinity
    def register(self, callback, delay):
        self.observers.append({delay, callback})
