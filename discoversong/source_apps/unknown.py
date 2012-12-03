from discoversong.source_apps import DiscoversongSourceApp

class UnknownApp(DiscoversongSourceApp):
  @staticmethod
  def parse(subject, body):
    return subject, ''
  
  @staticmethod
  def parse_tweet(tweet):
    return tweet.replace('#', '').replace('@', '').replace('_', ' '), ''
