#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# wave.open
import wave


def readAudio(filepath):
  f = wave.open(filepath, 'rb')
  params = f.getparams()
  nchannels, sampwidth, framerate, nframes = params[:4]
  str_data = b''+ f.readframes(nframes)
  return str_data, sampwidth, framerate

def writeAudio(out_filename, data):
  file = wave.open(out_filename, 'wb')
  file.setnchannels(1)
  file.setsampwidth(2)
  file.setframerate(16000)
  file.writeframes(data)
  file.close()


if __name__ == "__main__":
  # 读取
  filePath = 'wav/001.wav'
  byte_Data = readAudio(filePath)
  # 保存
  new_file = 'new_wav/001.wav'
  writeAudio(new_file, byte_Data)