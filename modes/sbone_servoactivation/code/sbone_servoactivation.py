from mpf.core.mode import Mode
from mpf.core.delays import DelayManager
import random

class sbone_servoactivation(Mode):

    def mode_init(self):
        self.log.info('sbone_servoactivation_mode_init')
        self.delay = DelayManager(self.machine.delayRegistry)

    def mode_start(self, **kwargs):
        self.log.info('sbone_servoactivation mode_start')

        self.add_mode_event_handler('balldevice_bd_sbone_ball_eject_attempt', self.eject_a_ball)

    def eject_a_ball(self, **kwargs):
        self.machine.events.post('sbone_ejecting_a_ball')
        self.machine.events.post('sbone_lock_servo_open')
        
        if self.machine.ball_devices.bd_sbone.available_balls == 3:
            self.log.info('activating delay for 3 balls')
            delay = 100
        elif self.machine.ball_devices.bd_sbone.available_balls == 2:
            self.log.info('activating delay for 2 balls')
            delay = 120
        elif self.machine.ball_devices.bd_sbone.available_balls == 1:
            self.log.info('activating delay for 1 balls')
            delay = 140
        else:
            self.log.info('activating delay for unknown balls')
            delay = 140

        self.delay.add(callback=self._post_event, ms=delay, event='sbone_lock_servo_closed')
        self.delay.add(callback=self._post_event, ms=600, event='sbone_ball_has_probably_been_released')

    def _post_event(self, event):
        self.machine.events.post(event)

    def mode_stop(self, **kwargs):
        self.machine.events.post('sbone_servoactivation_mode_ended')
        self.log.info('sbone_servoactivation_mode_stop')


