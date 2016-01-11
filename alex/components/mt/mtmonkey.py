#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is PEP8-compliant. See http://www.python.org/dev/peps/pep-0008.
from __future__ import unicode_literals
import urllib2
import json

from alex.components.mt.base import MTInterface
from alex.components.mt.exceptions import MTException

class MTMonkeyMT(MTInterface):

    """
    Uses MTMonkey web service for translation.

    """

    def __init__(self, cfg):
        super(MTMonkeyMT, self).__init__(cfg)
        self.url = self.cfg['MT']['MTMonkey']['url']

    def get_translation_hypotheses(self, text):
        params = dict(self.cfg['MT']['MTMonkey']['parameters'])
        params['text'] = text

        data = json.dumps(params)
        header = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
                  "Content-Type": "application/json"}

        request = urllib2.Request(self.url, data, header)
        json_hypotheses = urllib2.urlopen(request).read()

        if self.cfg['MT']['MTMonkey']['debug']:
            self.syslog.debug(json_hypotheses)

        return json_hypotheses

    def flush(self):
        pass

    def translate(self, asr_hyp):
        """
        Translate the given ASR hypothesis.
        """

        best_asr_hyp = unicode(asr_hyp.get_best()).lower()
        if best_asr_hyp == '':
            return ['']

        if '_other_' != best_asr_hyp:
            try:
                json_hypotheses = self.get_translation_hypotheses(best_asr_hyp)
            except (urllib2.HTTPError, urllib2.URLError) as e:
                self.syslog.exception('MTMonkey connection error: %s' % unicode(e))
                return ['__error__']

            try:
                monkey_hyp = json.loads(json_hypotheses)

                if 'errorCode' in monkey_hyp and monkey_hyp['errorCode'] == 0:
                    nblist = ['']
                    sep = ''
                    for sentence in monkey_hyp['translation']:
                        nblist[0] += sep + sentence['translated'][0]['text']
                        sep = ' '
                else:
                    if 'errorCode' in monkey_hyp and 'errorMessage' in monkey_hyp:
                        self.syslog.exception('MTMonkey error #%d: %s' % (monkey_hyp['errorCode'], monkey_hyp['errorMessage']))
                        return ['__error__']
                    else:
                        self.syslog.exception('MTMonkey error: unexpected response %s' % (json_hypotheses))
                        return ['__error__']
            except:
                self.syslog.exception('MTMonkey error: error parsing response %s' % (json_hypotheses))
                return ['__error__']
        else:
            nblist = ['_other_']

        return nblist
