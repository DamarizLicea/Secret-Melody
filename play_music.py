from pygame import mixer
import time
mixer.init()
mixer.music.load("melodia.mid")
mixer.music.play()

while True:
    time.sleep(0.1)

