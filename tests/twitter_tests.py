import unittest

class TwitterTests(unittest.TestCase):
  
  def test_twitter(self):
    from discoversong.twitter import api as twitter_api
    api = twitter_api()
    self.assertEqual(api.me().name, "Discoversong")
