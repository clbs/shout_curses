import vlc
import time

class VLCPlayer:
  def __init__(self):
    self.instance = vlc.Instance("--input-repeat=-1", "--fullscreen", "--verbose=-1")
    self.instance.log_unset()
    self.player = self.instance.media_player_new()
    

  def stream_media(self, media):
    stream_instance = self.instance.media_new(media)
    self.player.set_media(stream_instance)
    self.player.play()

  def volume_up(self):
    if self.player.audio_get_volume() >= 190:
      self.player.audio_set_volume(200)
    else:
      self.player.audio_set_volume(self.player.audio_get_volume() + 10)
    return str(self.player.audio_get_volume())

  def volume_down(self):
    if self.player.audio_get_volume() <= 10:
      self.player.audio_set_volume(0)
    else:
      self.player.audio_set_volume(self.player.audio_get_volume() - 10)
    return str(self.player.audio_get_volume())

  def toggle_mute(self):
    muted = not self.player.audio_get_mute()
    self.player.audio_set_mute(muted)
    return "[Muted]" if muted else "       "

  def get_mute(self):
    muted = not self.player.audio_get_mute()
    return "[Muted]" if muted else "       "

  def toggle_play(self):
    if self.player.is_playing() == 0:
      self.player.play()
      return "Playing"
    elif self.player.is_playing() == 1:
      self.player.stop()
      return "Stopped" 
  
  def get_play(self):
    if self.player.is_playing() == 0:
      self.player.play()
      return "Playing"
    elif self.player.is_playing() == 1:
      self.player.stop()
      return "Stopped" 
  
  def play(self):
    self.player.play()

  def stop(self):
    self.player.stop()

  def close(self):
    self.instance.release()

  def get_volume(self):
    return str(self.player.audio_get_volume())

  

