import pyaudio
import sounddevice as sd
from collections import deque
import math
import audioop
import time


def listen(dev, threshold):
    # print(sd.query_devices())
    sd.default.device[0] = dev
    print('正在监听水声...')
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 18000
    THRESHOLD = threshold
    SILENCE_LIMIT = 1

    success = 0
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    rel = RATE / CHUNK
    slid_win = deque(maxlen=SILENCE_LIMIT * int(rel))
    start_time = time.time()
    while True:
        try:
            cur_data = stream.read(CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            # print(sum(slid_win))
            if sum(slid_win) > THRESHOLD:
                print("上钩...")
                success = 1
                break
            if time.time() - start_time > 20:
                print('超时为上钩...')
                break
        except IOError:
            break

    stream.close()
    audio.terminate()
    if success == 1:
        return True
    else:
        return False
