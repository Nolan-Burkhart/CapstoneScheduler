#My NolanCFG Reader
import re

class settings:
  settings = dict()
  def __init__(self):
    self.settings = dict()
  def get_setting(self, name):
    if name in self.settings.keys():
      return self.settings[name]
    else:
      assert False, "Invalid Setting Requested: "+name
      return "Not Found"
  def add_setting(self, name, value):
    self.settings[name] = value


SEARCHES = ["(?P<key>.*) = (?P<value>.*) as (?P<type>.*)","(?P<key>.*) = (?P<value>.*)"]

class settings_loader:
  f = ""
  result = settings()
  def __init__(self, f):
    self.f = f
    self.result = settings()
    self.load_settings()
  def load_settings(self):
    file_reader = open(self.f) #open our file
    line = file_reader.readline() #read first line
    while line:
      unignored_key = line.find("-+")
      if unignored_key != -1:
        line = line[:unignored_key]
      if len(line) > 1:
        for search in SEARCHES:
          match = re.search(search,line)
          if match is not None:
            self.line_handler(search,line,match)
            break
      line = file_reader.readline()
    return self.result
  def line_handler(self, search, text, regex):
    #dont you love not having switch statements
    if search == "(?P<key>.*) = (?P<value>.*) as (?P<type>.*)":
      if regex.group("type") == "String":
        self.result.add_setting(regex.group("key"),str(regex.group("value")))
      elif regex.group("type") == "Int":
        self.result.add_setting(regex.group("key"),int(regex.group("value")))
        print(text)
    elif search == "(?P<key>.*) = (?P<value>.*)":
      self.result.add_setting(regex.group("key"),regex.group("value"))