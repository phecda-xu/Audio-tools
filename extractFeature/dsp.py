#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 预加重,分帧,加窗
import numpy as np
from scipy.fftpack import dct

# 预加重
def preEmphasis(signal):
    '''
    # TODO 预加重
    :param signal:         原始音频数据，array
    :return:               预加重后的音频数据，array
    '''
    pre_emphasis = 0.97
    emphasized_signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])
    return emphasized_signal


# 分帧
def enFrame(frame_size, frame_stride, sample_rate, signal):
  '''
  # TODO 分帧
  :param frame_size:        帧大小,单位s,float
  :param frame_stride:      步大小,单位s,float
  :param sample_rate:       采样率,int
  :param signal:            音频数据,list
  :return:                  分帧后的音频数据,array
  '''
  frame_length = int(round(frame_size * sample_rate))
  frame_step = int(round(frame_stride * sample_rate))
  signal_length = len(signal)
  num_frames = int(np.ceil(float(np.abs(signal_length - frame_length)) / frame_step + 1))
  pad_signal_length = num_frames * frame_step + frame_length
  z = np.zeros((pad_signal_length - signal_length))
  pad_signal = np.append(signal, z)
  indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + np.tile(
    np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
  frames = pad_signal[np.mat(indices).astype(np.int32, copy=False)]
  return frame_length, frames


# 加窗
def HMWindows(frame_length, frames):
    '''
    TODO
    :param frame_length:     每一帧音频采样点数,int
    :param frames:           帧音频数据,array.shape:(len(frames), frame_length)
    :return:                 shape:(len(frames), frame_length)
    '''
    hamming = np.hamming(frame_length)   # 0.54 - 0.46 * np.cos((2 * np.pi * n) / (frame_length - 1))
    frames *= hamming                    # (len(frames), frame_length) * (frame_length,) = (len(frames), frame_length)
    return frames


# 傅里叶变换
def FFT(frames, nfft=512):
    '''
    TODO 傅里叶变换
    :param frames:            帧音频数据,array.shape:(len(frames), frame_length)
    :param nfft:              傅里叶变换,nfft通常取256或者512
    :return:                  shape:(numframes,257)或者(numframes,128)
    '''
    fft_frames = np.fft.rfft(frames, nfft)
    return fft_frames


# 功率谱
def powerSpectrum(frames):
    '''
    TODO 功率谱
    :param frames:             shape:(numframes,257)或者(numframes,128)
    :return:                   shape:(numframes,257)或者(numframes,128)
    '''
    nfft = (frames.shape[1]-1)*2                       # (257-1)*2 = 512
    mag_frames = np.absolute(frames)
    pow_frames = ((1.0 / nfft) * ((mag_frames) ** 2))  # Power Spectrum
    return pow_frames


# 梅尔滤波
def melFilter(frames, nfilt, sample_rate):
    '''
    # TODO 梅尔滤波
    :param frames:        帧数据,array
    :param nfilt:         滤波器数量,int
    :param sample_rate:   采样率,int
    :return:              滤波后结果,array.shape:(numframes,40)
    '''
    nfft = (frames.shape[1]-1)*2                                         # (257-1)*2 = 512
    low_freq_mel = 0
    high_freq_mel = (2595 * np.log10(1 + (sample_rate / 2) / 700))
    mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)     # Equally spaced in Mel scale
    hz_points = (700 * (10 ** (mel_points / 2595) - 1))                  # Convert Mel to Hz
    bin = np.floor((nfft + 1) * hz_points / sample_rate)
    fbank = np.zeros((nfilt, int(np.floor(nfft / 2 + 1))))
    for m in range(1, nfilt + 1):
        f_m_minus = int(bin[m - 1])                                      # left
        f_m = int(bin[m])                                                # center
        f_m_plus = int(bin[m + 1])                                       # right
        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
    filter_banks = np.dot(frames, fbank.T)
    filter_banks = 20 * np.log10(filter_banks)
    return filter_banks


# DCT变换
def DCT(filter_banks, num_ceps=10):
    '''
    TODO dct变换
    :param filter_banks:               array,
    :param num_ceps:                   mfcc 特征维数，一般取13，默认10
    :return:                           array.shape(): (numframes,10)
    '''
    dct_array = dct(filter_banks, type=2, axis=1, norm='ortho')[:, 1: (num_ceps + 1)]
    return dct_array


if __name__ == "__main__":
    pass