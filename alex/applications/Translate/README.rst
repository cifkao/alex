TranslateHub
============

This application provides spoken language translation.

If you want to run ``slt_hub.py`` on some specific phone number, then specify the appropriate extension config:

::

  $ ./slt_hub.py -c slt_hub_SRC_TGT.cfg  ../../resources/private/ext-PHONENUMBER.cfg


After collection desired number of calls, use ``copy_wavs_for_transcription.py`` to extract the wave files from
the ``call_logs`` subdirectory for transcription. The files will be copied into into ``SLT-WAVs`` directory.

These calls must be transcribed by the Transcriber or some similar software.
