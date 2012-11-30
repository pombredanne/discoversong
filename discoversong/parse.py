def has_parts(text, lead=None, separator=None, terminator=None):
  if lead is not None:
    lead_loc = text.find(lead)
    if lead_loc < 0:
      return False
  else:
    lead_loc = 0
  sep_loc = text.find(separator, lead_loc)
  if sep_loc < 0:
    return False
  if terminator is not None:
    term_loc = text.find(terminator, sep_loc)
    if term_loc < 0:
      return False
  return True

def get_parts(text, lead=None, separator=None, terminator=None, reversed=False):
  assert has_parts(text, lead, separator, terminator=terminator)
  if lead is None:
    part1_start = 0
  else:
    part1_start = text.find(lead) + len(lead)
  part1_end = text.find(separator, part1_start)
  part1 = text[part1_start:part1_end]
  
  part2_start = part1_end + len(separator)
  if terminator:
    part2_end = text.find(terminator, part2_start)
    part2 = text[part2_start:part2_end]
  else:
    part2 = text[part2_start:]
  
  return (part1, part2) if not reversed else (part2, part1)

def parse_vcast(subject, body):
  lead = 'Music ID: "'
  separator = '" by '
  
  if not has_parts(subject, lead, separator):
    raise ValueError('not VCast!')
  return get_parts(subject, lead, separator)

def parse_shazam(subject, body):
  lead = 'I just used Shazam to tag '
  separator = ' by '
  terminator = '.'
  
  if not has_parts(subject, lead, separator, terminator):
    raise ValueError('Not Shazam!')
  return get_parts(subject, lead, separator, terminator)

def parse_shazam2(subject, body):
  expected_subject = 'I just used Shazam'
  lead = 'I just used #Shazam to discover '
  separator = ' by '
  terminator = '.'

  if subject != expected_subject or not has_parts(body, lead, separator, terminator):
    raise ValueError('Not Shazam2!')
  return get_parts(body, lead, separator, terminator)

def parse_soundhound(subject, body):
  lead = 'Just found '
  separator = ' by '
  terminator = ' on #SoundHound'
  
  if not has_parts(body, lead, separator, terminator):
    raise ValueError('Not SoundHound!')
  return get_parts(body, lead, separator, terminator)

def parse_musixmatch(subject, body):
  lead = 'I just used @musixmatch to discover '
  separator = ' by '
  terminator = ' #lyrics'
  
  if not has_parts(body, lead, separator, terminator):
    raise ValueError('Not MusixMatch!')
  return get_parts(body, lead, separator, terminator)

def parse_trackid(subject, body):
  lead = 'Check out '
  separator = ' by '
  terminator = '! I just found it using TrackID'
  
  if not has_parts(body, lead, separator, terminator):
    raise ValueError('Not TrackID!')
  return get_parts(body, lead, separator, terminator)

def parse_redlaser(subject, body):
  lead = "Check out '"
  separator = ' - '
  terminator = "' from RedLaser!"
  
  if not has_parts(subject, lead, separator, terminator):
    raise ValueError('Not RedLaser!')
  return get_parts(lead, separator, terminator, reversed=True)

def parse_unknown(subject, body):
  
  return subject, ''

def parse(subject, body):
  
  parsers = [parse_vcast,
             parse_shazam,
             parse_shazam2,
             parse_soundhound,
             parse_musixmatch,
             parse_trackid,
             parse_redlaser,
             parse_unknown] # this should always be last
  
  for parse in parsers:
    try:
      parsed = parse(subject, body)
      return parsed
    except Exception as ex:
      print ex.message
      continue
  raise ValueError('at least the unknown parser should have worked!')

