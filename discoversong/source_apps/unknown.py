from discoversong.source_apps import DiscoversongSourceApp

class UnknownApp(DiscoversongSourceApp):
  def parse(self, subject, body):
    return subject, ''
  
  def parse_tweet(self, tweet):
    return tweet.replace('#', '').replace('@', '').replace('_', ' '), ''
