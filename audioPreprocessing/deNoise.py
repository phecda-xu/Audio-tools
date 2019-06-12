# coding: utf-8
# python3
# 降噪
import numpy as np
import math



def enFrame(num_frames, frame_step, frame_length, emphasized_signal):
  '''
  # TODO 加窗分帧
  :param num_frames:        帧数,int
  :param frame_step:        步长,int
  :param frame_length:      帧长,int
  :param emphasized_signal: 预加重后的音频,list
  :return:                  分帧后的音频数据,array
  '''
  signal_length = len(emphasized_signal)
  pad_signal_length = num_frames * frame_step + frame_length
  z = np.zeros((pad_signal_length - signal_length))
  pad_signal = np.append(emphasized_signal, z)
  indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + np.tile(
    np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
  frames = pad_signal[np.mat(indices).astype(np.int32, copy=False)]
  return frames


def wienerFilter(YY, silentFrameNo, noise_est):
  '''
  # TODO 维纳滤波
  :param YY:
  :param silentFrameNo:
  :param noise_est:
  :return:
  '''
  a = 0.95
  Gain = np.ones(noise_est.shape)
  X = np.zeros(YY.shape)
  last_post_SNR = Gain
  frame_Num = len(YY[0])
  for i in range(silentFrameNo, frame_Num):
    current_post_SNR = (YY[:, i] ** 2) / noise_est
    prior_SNR = a * (Gain ** 2) * last_post_SNR + (1 - a) * np.maximum(current_post_SNR - 1, 0)
    last_post_SNR = current_post_SNR
    Gain = prior_SNR / (prior_SNR + 1) + 0.0001
    X[:, i] = Gain * YY[:, i]
  return X


def addOverlap(f, wnd, inc):
  '''
  # TODO
  :param f:
  :param wnd:
  :param inc:
  :return:
  '''
  [m, n] = f.shape
  w = wnd.T
  n_buf = math.ceil(n / inc)
  buf_len = n + (m - 1) * inc

  y_temp = np.zeros((buf_len, n_buf))
  temp_value = np.multiply(f, np.tile(w, (m, 1)))                               # 给每一帧进行加窗
  temp_1 = np.tile(np.arange(n), (m, 1))
  temp_2 = np.array(range(m)).T * inc
  temp_3 = ((np.arange(m).T) % n_buf) * buf_len
  temp_index = temp_1 + np.tile(temp_2 + temp_3, (n, 1)).T
  y_temp = y_temp.flatten()
  temp_index = temp_index.flatten()

  y_temp[temp_index] = temp_value.flatten()
  y_temp = y_temp.reshape(n_buf, buf_len)
  y = np.sum(y_temp, 0)
  return y


def wienerSpeechEhancement(x, fs, model_settings):
  '''
  # TODO
  # array_buffer = np.fromstring(bite_buffer, dtype=np.short)
  # temp_buffer = b''.join([struct.pack('h', d) for d in buffer])
  #
  # rfft的另一种实现
  # Y = np.fft.fft(f, N_fft)
  # Y = Y.T
  # [m, n] = Y.shape
  # Y = Y[0:int(m / 2) + 1, :]
  :param x:
  :param fs:
  :param model_settings:
  :return:
  '''
  frame_length = model_settings['window_size_samples']                      # 窗长，即每一帧的长度
  frame_step = model_settings['window_stride_samples']                      # 步长，
  num_frames = model_settings['spectrogram_length']                         # 帧数
  IS = 0.2                                                                  # 估计噪声的静默音频长度
  N_fft = 512                                                               # 傅里叶变换的点数

  f = enFrame(num_frames, frame_step, frame_length, x)                      # 分帧

  wnd = np.hamming(frame_length)
  f *= wnd                                                                  # 加窗，汉明窗

  silentFrameNo = int((IS * fs - frame_length) / (0.5 * frame_length) + 1)  # 静默帧数

  Y = np.fft.rfft(f, N_fft)                                                 # 对512个点进行FFT变换，得到257个
  Y = Y.T

  YPhase = np.angle(Y)
  YY = np.abs(Y)
  noise_est = np.mean((YY[:, 0:silentFrameNo]) ** 2, 1)
  X = wienerFilter(YY, silentFrameNo, noise_est)                            #  wiener滤波
  XX = np.multiply(X, np.exp(1j * YPhase))

  if (np.mod(len(f[0]), 2)):                                                # 将257个点恢复成512个点
    XX = np.row_stack((XX, np.flipud(np.conj(XX[0:, :]))))
  else:
    XX = np.row_stack((XX, np.flipud(np.conj(XX[1:-1, :]))))

  ss_out = np.fft.ifft(XX.T)                                                # 进行IFFT变换恢复到时域
  ss_out = ss_out[:, 0:len(wnd)]
  s2_out = np.real(ss_out)

  output = addOverlap(s2_out, wnd, frame_step)
  output = output.astype(int)
  return output
