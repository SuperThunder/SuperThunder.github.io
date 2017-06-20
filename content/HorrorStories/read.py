def main():
    import time # for sleeping - waiting without busy loops
    import os # for clearing the console
    #import threading # for later

    inputqueue = []
    CurrentStory = 0
    stories = []
    
    # Handle the initial case of setting up the program
    def init():
        nonlocal stories
        with open("horror.txt", 'r') as horrorfile:
            content = horrorfile.read()
            stories = content.split('-'*77)
            print("Stories: %d\n"%len(stories))
        
        
    
    # Handles the actual printing of the text; including whether or not to clear
    def display(text, clear=True):
        if( clear == True ):
            os.system('clear')

        print(text)
    
    
    # Main control loop - handles showing text
    def control():
        nonlocal CurrentStory # get around namespace issue - we can fix this later with OOP
        nonlocal stories
        
            
        while True:
            display( stories[CurrentStory] )
            WaitForInput()
            command = inputqueue.pop(0)
            # f: move forward a story
            if( command == 'f' or command == '' ):
                # Don't want to show a story that doesn't exist
                if( CurrentStory < len(stories) ):
                    CurrentStory += 1
                
            # b: move backward
            elif( command == 'b' ):
                if( CurrentStory > 0 ):
                    CurrentStory -= 1

            # Allow user to directly type in story to jump to
            elif( command.isnumeric() ):
                if( int(command) > 0 and int(command) < len(stories) ):
                    CurrentStory = int(command)
                    
            # else: input error
            else:
                # Do nothing on invalid input for now
                pass            
    
    
    # Input function
    def WaitForInput():
        print("\nCurrent: %d\tCommand: "%CurrentStory,)
        inputqueue.append( input() )

    # Init first to display the first story
    init()
    # After that go into control which has a loop
    control()

    return 0

main()
