# Audio-tools
Demos about read and write audio file

- 音频信息

> Duration: 00:00:05.41, bitrate: 256 kb/s

> Stream #0:0: Audio: pcm_s16le ([1][0][0][0] / 0x0001), 16000 Hz, 1 channels, s16, 256 kb/s

## 目录

- open() 方法

- wave.open() 方法

- soundfile 方法

- scipy.io 方法


## 1、open() 方法

#### 1.1、安装

```
无
```

#### 1.2、读

```
流数据长度： len(data[44:]) = 173088 
时长验证  ：173088/(2*16000) = 5.409s 

data[:44] : b'RIFFD\xa4\x02\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x00\x00\x02\x00\x10\x00data \xa4\x02\x00'
data[44:] ：b'\xf4\xff\xf3\xff\xf5\xff\xf9\xff\xf7\xff\xf1\xff\xf0\xff\xef\xff\xf0\xff\xef\xff\xf5\xff\xf4\xff\xfb\xff\xf9\xff\xf4\xff\xf6\xff\xf2\xff\xf5\xff...'
```

```
转换成数组格式
$ np.fromstring(data[44:],dtype=np.short)

array([-12, -13, -11, -7, -9, -15, ..., -54, -52, -57], dtype=int16)
```
#### 1.3、写

```
包含头文件信息的二进制数据直接写入文件中。
即，使用open方法读取得到的全部的data可以直接使用write指令写入 .wav 文件中。

如果不是通过open()方法获取的数据，需要在数据前面加上头信息，再保存。

如果将二进制数据转换成数组数据则需要使用soundfile或者scipy.io
```

## 2、wave.open() 方法

#### 2.1、安装

```
$ pip install wave
```

#### 2.2、读
```
流数据长度： len(data) = 173088 
时长验证  ：173088/(2*16000) = 5.409s 
sampwidth 表示位宽
framerate 即采样率
data：b'\xf4\xff\xf3\xff\xf5\xff\xf9\xff\xf7\xff\xf1\xff\xf0\xff\xef\xff\xf0\xff\xef\xff\xf5\xff\xf4\xff\xfb\xff\xf9\xff\xf4\xff...'
```
```
转换成数组格式
$ np.fromstring(data[44:],dtype=np.short)

array([-12, -13, -11, -7, -9, -15, ..., -54, -52, -57], dtype=int16)
```
#### 2.3、写

```
wave.open 方法读取的byte_data 数据不包括音频的文件头，所以可以在使用同样的方法进行保存时，需要设置相应的头信息；

不用wave.open的方法保存，则可以自己生成头文件信息，拼接上去再使用open的方法保存。

如果将二进制数据转换成数组数据则需要使用soundfile或者scipy.io
```


## 3、soundfile 方法



## 4、scipy.io 方法



## 