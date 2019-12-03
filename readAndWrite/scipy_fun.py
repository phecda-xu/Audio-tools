#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# scipy.io
from scipy.io import wavfile

# 读
sample_rate, signal = wavfile.read('../wav/003.wav')


# 写
wavfile.write('new_wav/001.wav', sample_rate, signal)