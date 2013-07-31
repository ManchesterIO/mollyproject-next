__author__ = 'chris'


class NullStats(object):

    class DummyTimer(object):

        def __enter__(self):
            pass

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    def timer(self, *args, **kwargs):
        return self.DummyTimer()

    def timing(self, *args, **kwargs):
        pass

    def incr(self, *args, **kwargs):
        pass

    def decr(self, *args, **kwargs):
        pass

    def gauge(self, *args, **kwargs):
        pass