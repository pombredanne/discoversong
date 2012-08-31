def parse_vcast(subject, body):
  
  lead = 'Music ID: "'
  separator = '" by '
  
  if subject.find(lead) < 0 or subject.find(separator) < 0:
    raise ValueError('not VCast!')
  
  title_start = subject.find(lead) + len(lead)
  title_end = subject.find(separator)
  
  title = subject[title_start:title_end]
  
  artist_start = title_end + len(separator)
  
  artist = subject[artist_start:]

  return title, artist

def parse_shazam(subject, body):
  
  separator =  '- '
  
  title_end = subject.find(separator)
  if title_end < 0:
    raise ValueError('not Shazam!')
  
  title = subject[:title_end]
  
  artist_start = title_end + len(separator)
  artist = subject[artist_start:]
  return title, artist

def parse_shazam2(subject, body):
  
  expected_subject = 'I just used Shazam'
  lead = 'I just used #Shazam to discover '
  separator = ' by '
  terminator = '.'

  if subject.find(expected_subject) < 0:
    raise ValueError('Shazam2 did not match expected subject')
  
  if body.find(lead) < 0:
    raise ValueError('Shazam2 did not find expected lead')
  lead_start = body.find(lead)
  if body.find(separator, lead_start) < 0:
    raise ValueError('Shazam2 did not find expected separator')
  separator_start = body.find(separator, lead_start)
  if body.find(terminator, separator_start) < 0:
    raise ValueError('Shazam2 did not find expected terminator')
  
  title_start = body.find(lead) + len(lead)
  title_end = body.find(separator, title_start)
  title = body[title_start:title_end]
  
  artist_start = title_end + len(separator)
  artist_end = body.find(terminator, artist_start)
  artist = body[artist_start:artist_end]
  
  return title, artist

def parse_unknown(subject, body):
  
  return subject, ''

def parse(subject, body):
  
  parsers = [parse_vcast,
             parse_shazam,
             parse_shazam2,
             parse_unknown] # this should always be last
  
  for parse in parsers:
    try:
      parsed = parse(subject, body)
      return parsed
    except Exception as ex:
      print ex.message
      continue
  raise ValueError('at least the unknown parser should have worked!')

