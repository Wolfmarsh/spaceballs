from mpf.core.mode import Mode
import random

class sbone_autoeject(Mode):

    def mode_init(self):
        self.log.info('sbone_autoeject mode_init')

    def mode_start(self, **kwargs):
        self.log.info('sbone_autoeject mode_start')
        self.machine.ball_devices.bd_sbone.config["auto_fire_on_unexpected_ball"] = True

    def mode_stop(self, **kwargs):
        self.machine.ball_devices.bd_sbone.config["auto_fire_on_unexpected_ball"] = False
        self.machine.events.post('sbone_autoeject mode_ended')
        self.log.info('sbone_autoeject mode_stop')


