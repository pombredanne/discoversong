from discoversong.source_apps.ericssontrackid import EricssonTrackIdApp
from discoversong.source_apps.musixmatch import MusixMatchApp
from discoversong.source_apps.redlaser import RedLaserApp
from discoversong.source_apps.soundhound import SoundHoundApp
from discoversong.source_apps.shazam import ShazamApp
from discoversong.source_apps.vcast_songid import VcastSongidApp
from discoversong.source_apps.unknown import UnknownApp

class SourceAppsManager(object):
  Shazam = ShazamApp
  SoundHound = SoundHoundApp
  MusixMatch = MusixMatchApp
  EricssonTrackId = EricssonTrackIdApp
  VcastSongid = VcastSongidApp
  RedLaser = RedLaserApp
  Unknown = UnknownApp
  
  ALL = (SoundHound, Shazam, MusixMatch, EricssonTrackId, VcastSongid, RedLaser)
  
  @staticmethod
  def by_appname(appname):
    for app in SourceAppsManager.ALL:
      if app.appname == appname:
        return app
    return None
