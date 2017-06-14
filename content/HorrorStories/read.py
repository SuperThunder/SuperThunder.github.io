with open("horror.txt", 'r') as horrorfile:
    filecont = horrorfile.read()
    stories = filecont.split('-'*77)
    print("Stories: %d"%len(stories))

import os
for story in stories:
    print(story)
    os.system('clear')
    input()
