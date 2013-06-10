from discoversong.source_apps.ericssontrackid import EricssonTrackIdApp
from discoversong.source_apps.musixmatch import MusixMatchApp
from discoversong.source_apps.soundhound import SoundHoundApp
from discoversong.source_apps.shazam import ShazamApp
from discoversong.source_apps.unknown import UnknownApp

class SourceAppsManager(object):
  Shazam = ShazamApp
  SoundHound = SoundHoundApp
  MusixMatch = MusixMatchApp
  EricssonTrackId = EricssonTrackIdApp
  Unknown = UnknownApp
  
  ALL = (SoundHound, Shazam, MusixMatch, EricssonTrackId)
  
  @staticmethod
  def by_appname(appname):
    for app in SourceAppsManager.ALL:
      if app.appname == appname:
        return app
    return None
  
  @staticmethod
  def all_capabilities():
    all_caps = list()
    cap_types = set()
    for app in SourceAppsManager.ALL:
      for cap in app.capabilities:
        if type(cap) not in cap_types:
          all_caps.append(cap)
          cap_types.add(type(cap))
    return all_caps
