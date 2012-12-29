import celery
import celery.apps.beat
import celery.beat

class Service(celery.Celery):

    def __init__(self):
        super(Service, self).__init__()
        self.periodic_tasks = []

    def init_cli_commands(self, manager):

        @manager.command
        def taskbeat():
            beat = celery.apps.beat.Beat(app=self)
            beat.scheduler_cls=Scheduler
            beat.run()

        @manager.command
        def taskworker():
            self.Worker().run_worker()

    def periodic_task(self, *args, **kwargs):
        crontab = kwargs.pop('crontab')
        task = self.task(*args, **kwargs)
        self.periodic_tasks[task.name] = {'task': task, 'schedule': crontab}
        return task


class Scheduler(celery.beat.PersistentScheduler):

    def setup_schedule(self):
        super(Scheduler, self).setup_schedule()
        print self._store
        self.merge_inplace(self.app.periodic_tasks)
