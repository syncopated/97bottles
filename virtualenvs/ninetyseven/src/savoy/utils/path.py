def append_third_party_path():
  import os, sys
  sys.path.append(os.path.join(os.path.dirname(__file__), '../third_party'))