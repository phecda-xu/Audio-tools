#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 读取双通道的MP3 并分别保存
import librosa
import soundfile as sf

# 读
stream, sr = librosa.load('wav/002.mp3', sr=8000, mono=False)

# 取通道0数据

signal_0 = stream[0]

# 取通道1数据

signal_1 = stream[0]

# 保存

sf.write('new_wav/001_0.wav', signal_0, samplerate=sr)
sf.write('new_wav/001_1.wav', signal_1, samplerate=sr)