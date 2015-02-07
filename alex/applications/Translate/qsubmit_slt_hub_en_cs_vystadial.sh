#!/bin/bash

qsubmit 'python slt_hub.py -c slt_hub_en_cs.cfg ../../resources/private/ext-vystadial-277278178.cfg gasr_private.cfg -t vrss_en.cfg vrss_private.cfg'
qsubmit 'python slt_hub.py -c slt_hub_en_cs.cfg ../../resources/private/ext-vystadial-277278178b1.cfg gasr_private.cfg -t vrss_en.cfg vrss_private.cfg'
qsubmit 'python slt_hub.py -c slt_hub_en_cs.cfg ../../resources/private/ext-vystadial-277278178b2.cfg gasr_private.cfg -t vrss_en.cfg vrss_private.cfg'
