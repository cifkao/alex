#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import time

from alex.components.hub.messages import Command, ASRHyp, MTHyp
from alex.components.mt.common import mt_factory
from alex.components.mt.exceptions import MTException
from alex.utils.procname import set_proc_name


class MT(multiprocessing.Process):
    """
    The MT component receives ASR hypotheses and translates them into
    another language.

    This component is a wrapper around multiple MT components which handles
    inter-process communication.
    """

    def __init__(self, cfg, commands, asr_hypotheses_in, mt_hypotheses_out,
                 close_event):
        """
        Initialises an MT object according to the configuration (cfg['MT']
        is the relevant section), and stores ends of pipes to other processes.

        Arguments:
            cfg: a Config object specifying the configuration to use
            commands: our end of a pipe (multiprocessing.Pipe) for receiving
                commands
            asr_hypotheses_in: our end of a pipe (multiprocessing.Pipe) for
                receiving ASR hypotheses (from ASR)
            mt_hypotheses_out: our end of a pipe (multiprocessing.Pipe) for
                sending MT hypotheses

        """

        multiprocessing.Process.__init__(self)

        # Save the configuration.
        self.cfg = cfg

        # Save the pipe ends.
        self.commands = commands
        self.asr_hypotheses_in = asr_hypotheses_in
        self.mt_hypotheses_out = mt_hypotheses_out
        self.close_event = close_event

        # Load the MT.
        self.mt = mt_factory(cfg)

    def process_pending_commands(self):
        """
        Process all pending commands.

        Available commands:
          stop() - stop processing and exit the process
          flush() - flush input buffers.
            Now it only flushes the input connection.

        Return True if the process should terminate.
        """

        while self.commands.poll():
            command = self.commands.recv()
            if self.cfg['MT']['debug']:
                self.cfg['Logging']['system_logger'].debug(command)

            if isinstance(command, Command):
                if command.parsed['__name__'] == 'stop':
                    return True

                if command.parsed['__name__'] == 'flush':
                    # Discard all data in input buffers.
                    while self.asr_hypotheses_in.poll():
                        self.asr_hypotheses_in.recv()

                    self.mt.flush()

                    self.commands.send(Command("flushed()", 'MT', 'HUB'))

                    return False

        return False

    def read_asr_hypotheses_write_mt_hypotheses(self):
        if self.asr_hypotheses_in.poll():
            data_asr = self.asr_hypotheses_in.recv()

            if isinstance(data_asr, ASRHyp):
                nblist = self.mt.translate(data_asr.hyp)
                fname = data_asr.fname

                if self.cfg['MT']['debug']:
                    s = []
                    s.append("MT Hypothesis")
                    s.append("-" * 60)
                    s.append("Nblist:")
                    s.append(unicode(nblist))
                    s.append("")
                    s = '\n'.join(s)
                    self.cfg['Logging']['system_logger'].debug(s)

                #self.cfg['Logging']['session_logger'].mt("user", fname, nblist)

                self.commands.send(Command('mt_translated(fname="%s")' % fname, 'MT', 'HUB'))
                self.mt_hypotheses_out.send(MTHyp(nblist, asr_hyp=data_asr.hyp))

            elif isinstance(data_asr, Command):
                self.cfg['Logging']['system_logger'].info(data_asr)
            else:
                raise MTException('Unsupported input.')

    def run(self):
        try:
            set_proc_name("Alex_MT")
            self.cfg['Logging']['session_logger'].cancel_join_thread()

            while 1:
                # Check the close event.
                if self.close_event.is_set():
                    print 'Received close event in: %s' % multiprocessing.current_process().name
                    return

                time.sleep(self.cfg['Hub']['main_loop_sleep_time'])

                s = (time.time(), time.clock())

                # process all pending commands
                if self.process_pending_commands():
                    return

                # process the incoming ASR hypotheses
                self.read_asr_hypotheses_write_mt_hypotheses()

                d = (time.time() - s[0], time.clock() - s[1])
                if d[0] > 0.200:
                    print "EXEC Time inner loop: MT t = {t:0.4f} c = {c:0.4f}\n".format(t=d[0], c=d[1])

        except KeyboardInterrupt:
            print 'KeyboardInterrupt exception in: %s' % multiprocessing.current_process().name
            self.close_event.set()
            return
        except:
            self.cfg['Logging']['system_logger'].exception('Uncaught exception in MT process.')
            self.close_event.set()
            raise

        print 'Exiting: %s. Setting close event' % multiprocessing.current_process().name
        self.close_event.set()
