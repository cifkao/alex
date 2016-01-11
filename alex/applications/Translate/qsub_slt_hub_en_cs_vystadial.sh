#!/bin/bash

qsub -cwd -j y -pe smp 6 -b y -o logs -S /bin/bash -N alex-1 python slt_hub.py -c slt_hub_en_cs.cfg ../../resources/private/ext-vystadial-277278178.cfg gasr_private.cfg speechtech_private.cfg -t vrss_en.cfg vrss_private.cfg -a kaldi.cfg
qsub -cwd -j y -pe smp 6 -b y -o logs -S /bin/bash -N alex-2 python slt_hub.py -c slt_hub_en_cs.cfg ../../resources/private/ext-vystadial-277278178b1.cfg gasr_private.cfg speechtech_private.cfg -t vrss_en.cfg vrss_private.cfg -a kaldi.cfg
#qsub -cwd -j y -pe smp 6 -b y -o logs -S /bin/bash -N alex-3 python slt_hub.py -c slt_hub_en_cs.cfg ../../resources/private/ext-vystadial-277278178b2.cfg gasr_private.cfg speechtech_private.cfg -t vrss_en.cfg vrss_private.cfg -a kaldi.cfg
