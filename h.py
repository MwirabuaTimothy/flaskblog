import readline
# for i in range(1, readline.get_current_history_length()+1):
  # commands += "%3d %s" % (i, readline.get_history_item(i))
def history():
  commands = ''
  for i in range(readline.get_current_history_length()):
      commands = readline.get_history_item(i + 1)
  print(commands)