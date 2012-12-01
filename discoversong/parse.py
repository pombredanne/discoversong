from discoversong.sources import SourceAppsManager

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

def parse(subject, body):
  # circular import
  from discoversong.source_apps.capabilities import Capabilities

  for source_app in SourceAppsManager.ALL + (SourceAppsManager.Unknown,):
    for cap in source_app.capabilities:
      if type(cap) == Capabilities.Email:
        try:
          return cap.parse(subject, body)
        except Exception as ex:
          print ex.message
          continue
  
  raise ValueError('at least the unknown parser should have worked!')

