# coding:utf-8
#
# Date:2019.06.10
# DEC:
#   record speech with pyaudio which controled by keyboard
import pyaudio
import threading
import wave
from pynput import keyboard


class Recorder(object):
    def __init__(self, chunk=1024, channels=1, rate=64000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []
        self._firstPress = 0
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

    def start(self):
        threading._start_new_thread(self.__recording, ())

    def __recording(self):
        self._running = True
        self._frames = []
        while self._running:
            data = self.stream.read(self.CHUNK)
            self._frames.append(data)
        self.stream.stop_stream()
        self.stream.close()
        self. p.terminate()

    def stop(self):
        self._running = False

    def save(self, filename):
        p = pyaudio.PyAudio()
        if not filename.endswith(".wav"):
            filename = filename + ".wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()
        print("Saved")

    def on_press(self,key):
        if key == keyboard.Key.space and self._firstPress == 0:
            print("Start recording")
            self._firstPress = 1
            self.start()
        elif key == keyboard.Key.space and self._firstPress == 1:
            print(".", end='')

    def on_release(self,key):
        if key == keyboard.Key.space:
            print("\nStop recording")
            self.stop()
            self.save("mytestrecord.wav")
            # print('signal value : ', signal)
            return False

    # 一直监听键盘事件，直到停止
    def start_listen(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__ == "__main__":
    aa = Recorder()
    aa.start_listen()