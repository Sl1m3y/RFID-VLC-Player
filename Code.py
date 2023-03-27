import serial
import time
import vlc
import os

if os.environ.get('DISPLAY','') == '':
   os.environ.__setitem__('DISPLAY', ':0.0')

s = serial.Serial('/dev/ttyACM0', 9600)
s.reset_input_buffer()


print("Waiting for Card")

rootdir = '/home/linaro/RFID-Reader/'
player = vlc.Instance()

media = vlc.MediaPlayer(f"{rootdir}IdleRick.mp4")

def getVideo(videoID: int):

   videoPool = {
      "16418414591" : 'Test1.mp4',
      "20319018280" : 'Test2.mp4',
      "1872105880" : 'Test3.mp4',
      "18724118180" : 'Test4.mp4',
      "1397115880" : 'Test5.mp4'
   }

   return videoPool.get(videoID, None)

def playVideo(video: str):
   global media

   media.stop()
   media = vlc.MediaPlayer(f"{rootdir}{video}")

   media.toggle_fullscreen()
   media.play()
   time.sleep(1)

def getSerialData():
   res = s.readline().decode('utf-8').rstrip()
   time.sleep(2)
   
   return res


def main():
   videoString = None
   while True:
      # If the serial buffer is not empty, get the video ID, reset the buffer, and wait 4 seconds
      if s.in_waiting > 0:
         videoString = getVideo(getSerialData())
         time.sleep(4)
         s.reset_input_buffer()

      # If the video is not playing and the videoString is not None, play the video
      if videoString == None and media.is_playing() == 0:
         playVideo("IdleRick.mp4")

      # If the video is playing and the videoString is not None, stop the video and play the new video
      if videoString != None and media.is_playing() == 1:
         playVideo(videoString)
         videoString = None

if __name__ == "__main__":
   main()
