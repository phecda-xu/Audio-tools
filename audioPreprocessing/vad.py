#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# VAD
import numpy as np
import math
import struct




def voiceActivityDetection(bite_buffer, sampleRate):
  '''
  # TODO 静音检测
  :param bite_buffer:   二进制的音频流数据，byte
  :param sampleRate:    音频采样率，int
  :return:              处理后的二进制音频流，byte
  '''
  array_buffer = np.fromstring(bite_buffer, dtype=np.short)                     # 二进制转数学形式
  t = 400                                                                       # 20ms
  frameLength = sampleRate * t // 1000                                          # 帧长
  frames = [array_buffer[i:i + frameLength] for i
            in range(0, len(array_buffer), frameLength)]
  entropys = []
  dics = {}
  for fid, frame in enumerate(frames):
    dic = {}
    for d in frame:
      if d in dic.keys():
        dic[d] = dic[d] + 1
      else:
        dic[d] = 1
      if d in dics.keys():
        dics[d] = dics[d] + 1
      else:
        dics[d] = 1
    ns = np.array([dic[key] for key in dic.keys()])
    ps = ns / len(frame)
    logps = [math.log(p) for p in ps]
    entropy = -sum(np.array(ps) * np.array(logps))
    entropys.append(entropy)
  enthreshold = np.mean(entropys)
  tags1 = np.array(entropys) > enthreshold*0.6
  tags = np.repeat(tags1, frameLength)[0:len(array_buffer)]
  buffer = []
  for i in range(len(array_buffer)):
    if tags[i]:
      buffer.append(array_buffer[i])
  temp_buffer = b''.join([struct.pack('h', d) for d in buffer])
  return temp_buffer
