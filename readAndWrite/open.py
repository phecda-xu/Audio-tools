#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# open
# 读取的音频数据包括了音频的头文件信息（包括采样率，音频时长，位宽等）；
# 前44位（从0开始）为头文件信息，声音内容的数据从第44位开始
# 头文件信息 data[:44],声音内容 data[44:]


def readAudio(filePath):
  '''
  读取音频
  :param filePath: 音频路径
  :return: 二进制数据
  open 的另外一种写法：
  with open(filePath, 'rb') as f:
      data = f.read()
  '''
  f = open(filePath, 'rb')
  data = f.read()
  return data


def writeAudio(filePath, buffer):
  '''
  保存音频
  :param filePath: 音频路径
  :param buffer: 包含头文件信息的二进制流数据
  :return:
  open 的另外一种写法：
  with open(filePath, 'wb') as f:
      f.write(data)
  '''
  file = open(filePath, 'wb')
  file.write(buffer)
  file.close()


if __name__ == "__main__":
  # 读取
  filePath = 'wav/001.wav'
  byte_Data = readAudio(filePath)
  # 保存
  new_file = 'new_wav/001.wav'
  writeAudio(new_file, byte_Data)