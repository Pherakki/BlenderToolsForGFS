from .Counter import Counter


class OffsetMarker:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, obj, attr):
        def fn(x):
            setattr(obj, attr, x)
        self.subscribers.append(fn)
    
    def notify(self, position):
        for callback in self.subscribers:
            callback(position)


class OffsetTracker(Counter):
    def __init__(self):
        super().__init__()
