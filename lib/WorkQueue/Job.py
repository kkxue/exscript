import threading, sys

class Job(threading.Thread):
    def __init__(self, global_context, action, *args, **kwargs):
        threading.Thread.__init__(self)
        self.global_context = global_context
        self.local_context  = {}
        self.action         = action
        self.logfile        = None
        self.logfile_lock   = None
        self.debug          = kwargs.get('debug', 0)
        self.action.debug   = self.debug
        action.signal_connect('data_received', self._on_log_data_received)
        action.signal_connect('notify',        self._on_log_data_received)


    def _on_log_data_received(self, name, data):
        sys.stdout.write(data)


    def run(self):
        """
        """
        if self.debug:
            print "Job running: %s" % self
        try:
            self.action.execute(self.global_context, self.local_context)
        except Exception, e:
            print 'Job "%s" failed: %s' % (self.getName(), e)
            if self.debug:
                raise
