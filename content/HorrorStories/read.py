def main():
	
	import time # for sleeping - waiting without busy loops
	#import threading # for later
	inputqueue = []
	CurrentStory = 0
	
	# Main control loop - handles showing text
	def control():
		import os # for clearing the console
		stories = []
		with open("horror.txt", 'r') as horrorfile:
			content = horrorfile.read()
			stories = content.split('-'*77)
			print("Stories: %d\n"%len(stories))
			
		
		while True:
			inputqueue.pop(0)
			# f: move forward a story
			
			# b: move backward
			
			# else: input error
		
	
	# Input function
	def input():
		print("\nCommand: ",)
		inputqueue.append( input() )


	control()


main()
