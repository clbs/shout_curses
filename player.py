import vlc
import time

class VLCPlayer:
  def __init__(self):
    self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
    self.instance.log_unset()
    self.player = self.instance.media_player_new()

  def stream_media(self, media):
    stream_instance = self.instance.media_new(media)
    self.player.set_media(stream_instance)
    self.player.play()

  def volume_up(self):
    if self.player.audio_get_volume() >= 90:
      self.player.audio_set_volume(200)
    else:
      self.player.audio_set_volume(self.player.audio_get_volume() + 10)

  def volume_down(self):
    if self.player.audio_get_volume() <= 10:
      self.player.audio_set_volume(0)
    else:
      self.player.audio_set_volume(self.player.audio_get_volume() - 10)
  
  def play(self):
    self.player.play()

  def stop(self):
    self.player.stop()

  def close(self):
    self.instance.release()

  def get_volume(self):
    return self.player.audio_get_volume()

  

