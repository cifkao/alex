#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is PEP8-compliant. See http://www.python.org/dev/peps/pep-0008.
from __future__ import unicode_literals

class MTInterface(object):

    """
    This class basic interface which has to be provided by all MT modules to
    fully function within the Alex project.

    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.syslog = cfg['Logging']['system_logger']

    def flush(self):
        """
        Should reset the module immediately in order to be ready for next translation

        """
        raise MTException("Not implemented")

    def translate(asr_hyp):
        """
        Translate the given ASR hypothesis.
        """
        raise MTException("Not implemented")
