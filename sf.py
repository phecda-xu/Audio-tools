#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# soundfile
import soundfile as sf

# 读
signal, samplerate = sf.read('wav/001.wav',dtype='int16')

# 写
sf.write('new_wav/001.wav', signal, samplerate)

