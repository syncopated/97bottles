def unsmartypants(value):
  """
  Normalizes a string which has been processed by smartypants.py.
  """
  try:
    import smartypants
    return smartypants.smartyPants(value, '-1')
  except ImportError:
    return value