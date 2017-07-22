from mpf.core.mode import Mode
import random

class dead_flip(Mode):

    def mode_init(self):
        self.log.info('dead_flip mode_init')

        self.dead_flip_sequence = ["B","L","L","L","L","R","L","L","L","L","L","R","L","R","R"]
    def mode_start(self, **kwargs):
        self.log.info('dead_flip mode_start')
        self.sequence_pos = 0
        self.add_mode_event_handler('sw_left_flipper', self.flipper_left)
        self.add_mode_event_handler('sw_right_flipper', self.flipper_right)
        self.add_mode_event_handler('both_flippers_one', self.both_flippers)

    def both_flippers(self, **kwargs):
        if self.sequence_pos == 0:
            self.machine.events.post('dead_flip_code_sequence_started')
            self.sequence_pos = 1
        else:
            self.machine.events.post('resetting_dead_flip_code_sequence_and_starting')
            self.sequence_pos = 1

    def flipper_left(self, **kwargs):
        if self.sequence_pos > 0:
            self.machine.events.post('dead_flip_mode_got_left_flipper')
            if self.dead_flip_sequence[self.sequence_pos] == "L":
                self.machine.events.post('dead_flip_mode_correct_entry')
                self.sequence_pos = self.sequence_pos + 1
            else:
                self.machine.events.post('dead_flip_mode_incorrect_entry')
                self.sequence_pos = 0
            if self.sequence_pos >= len(self.dead_flip_sequence):
                self.machine.events.post('dead_flip_code_successfully_activated')
                self.sequence_pos = 0

    def flipper_right(self, **kwargs):
        if self.sequence_pos > 0:
            self.machine.events.post('dead_flip_mode_got_right_flipper')
            if self.dead_flip_sequence[self.sequence_pos] == "R":
                self.machine.events.post('dead_flip_mode_correct_entry')
                self.sequence_pos = self.sequence_pos + 1
            else:
                self.machine.events.post('dead_flip_mode_incorrect_entry')
                self.sequence_pos = 0
            if self.sequence_pos >= len(self.dead_flip_sequence):
                self.machine.events.post('dead_flip_code_successfully_activated')
                self.sequence_pos = 0

    def mode_stop(self, **kwargs):
        self.machine.events.post('dead_flip mode_ended')
        self.log.info('dead_flip mode_stop')


