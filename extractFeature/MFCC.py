#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFCC
import numpy
import scipy.io.wavfile
from extractFeature.dsp import *



def extractMfcc(sample_rate, signal):
    # 预加重
    emphasized_signal = preEmphasis(signal)
    # 分帧
    frame_length, frames = enFrame(0.04, 0.01, sample_rate, emphasized_signal)
    # 加上汉明窗
    frames = HMWindows(frame_length, frames)
    # 傅立叶变换
    fft_frames = FFT(frames, nfft=512)                              # nfft 通常为256 或者 512
    # 功率谱
    pow_frames = powerSpectrum(fft_frames)
    # 梅尔滤波
    filter_banks = melFilter(pow_frames, 40, sample_rate)
    # 应用离散余弦变换（DCT）去相关滤波器组系数并产生滤波器组的压缩表示
    dct_array = DCT(filter_banks, num_ceps=10)
    # 将正弦升降1应用于MFCC以降低已被声称在噪声信号中改善语音识别的较高MFCC
    (nframes, ncoeff) = dct_array.shape
    n = numpy.arange(ncoeff)
    cep_lifter =22
    lift = 1 + (cep_lifter / 2) * numpy.sin(numpy.pi * n / cep_lifter)
    mfcc = dct_array
    mfcc *= lift
    # 平均归一化MFCC
    mfcc -= (numpy.mean(mfcc, axis=0) + 1e-8)
    mfcc /= (numpy.std(mfcc, axis=0) + 1e-8)
    mfcc = mfcc.reshape(1,nframes, ncoeff)
    return mfcc


if __name__ == "__main__":
    sample_rate, signal = scipy.io.wavfile.read('../wav/001.wav')
    mfcc = extractMfcc(sample_rate, signal)
    print(1)