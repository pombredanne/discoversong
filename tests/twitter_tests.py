import unittest

class TwitterTests(unittest.TestCase):
  
  def test_twitter(self):
    from discoversong.twitter import api as twitter_api
    api = twitter_api()
    print api.get_account_settings()
    self.assertEqual(api.show_user(screen_name="dscvrsng")["name"], "Discoversong")
