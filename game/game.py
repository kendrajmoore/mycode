#!/usr/bin/python3
import os 
from os import system 
import sys
import time
import random
from time import sleep 

#colors

black = "\033[0;30m"
purple = "\033[0;35m"
blue = "\033[0;34m"
green = "\033[0;32m"
red = "\033[0;31m"
yellow = "\033[0;33m"
white = "\033[0;37m"

#score
fails = 0
passes = 0 

def scrollTxt(text):
    for char in text:
       sys.stdout.write(char)
       sys.stdout.flush()
       time.sleep(0.1)

def printStory():
    print(blue)
    scrollTxt("You were on a cruise but you get shipwrecked on an island. \n")
    scrollTxt("You discover it is inhabited only by billionaires playing a game. \n")
    time.sleep(1)
    print(red)
    scrollTxt("The most dangerous game. \n")
    print(blue)
    scrollTxt("At each new location you have to complete a challenge designed by the billionaires. \n")
    scrollTxt("You get three (3) chances to fail a challenge. \n")
    scrollTxt("If you can pass five (5) challenges, you can leave (no transportation provided back.) \n")
    scrollTxt("If you fail, ...... \n") 
    time.sleep(1)
    print(red)
    scrollTxt("YOU DIE !!!!!!\n") 
    print(black)
    
printStory()

def showInstructions():
    """Show the game instructions when called"""
    #print a main menu and the commands
    print('''
    RPG Game
    ========
    Commands:
      go [location]
      take [codename] 
      Make sure you are entering two words (follow directions)
    ''')

def showStatus():
    """determine the current status of the player"""
    # print the player's current location
    print('---------------------------')
    print(purple)
    print('You are at the ' + currentLocation)
    # print what the player has to do
    print("Challenges completed: ", challenges)
    # check if there's an challenge at that location, if so print it
    if "codename" in locations[currentLocation]:
          print("Codename for challenge: ", locations[currentLocation]['codename'])
    print("---------------------------")
  

# an inventory, which is initially empty
challenges = []

#score


def fail():
    global fails
    global passes
    value = random.randint(0, 1)
    if value == 0:
        fails = fails + 1
        print(red)
        scrollTxt("You failed \n")
        print(f"this is your number of fails: {fails} \n")
    else:
        print(green)
        passes = passes + 1
        scrollTxt("You passed \n")
        print(f"this is your number of passes: {passes} \n")


                	

# a dictionary linking a room to other rooms
locations = {

            'Boat Dock' : {
                  'south' : 'Beach',
                  'east'  : 'Ocean'
                },

            'Ocean' : {
                    'west': 'Boat Dock',
                   'south': 'Rainforest',
                   'codename' : 'skims',
                  'challenge': 'you have to work out for 3 hours wearing skims by Kim kardashian'
                },
            'Beach' : {
                'north': 'Boat Dock',
                'east': 'Rainforest',
                'south': 'Helipad',
                'codename': 'tesla',
                'challenge' : 'you have to pull a Telsa across the beach'
                },

            'Rainforest' : {
                  'north' : 'Ocean',
                  'west' : 'Beach',
                  'south' : 'Mountain',
                  'codename' : 'amazon',
                  'challenge' : 'you have to help build an Amazon warehouse in the actual Amazon'

                },
            'Helipad' : {
                  'east' : 'Mountain',
                  'north' : 'Beach',
                  'south' : 'Abandoned Building',
                  'codename': 'legos',
                  'challenge' : 'you have to build a functioning helicopter out of legos'
                },
            'Mountain' : {
                'north': 'Rainforest',
                'west' : 'Helipad',
                'south' : 'Server Room',
                'codename': 'microsoft',
                'challenge': 'Bill Gates orders you to build a computer out of legos'
            },
            'Abandoned Building' : {
                'north': 'Helipad',
                'east' : 'Server Room',
                'south' : 'Server Room Two',
                'codename': 'facebook',
                'challenge': 'you have a staring contest with Mark Zuckerberg'
            },
            'Server Room' : {
                'north' : 'Mountain',
                'west' : 'Abandoned Building',
                'south': 'Baseball field',
                'codename': 'google',
                'challenge': 'you have to wear google glasses for 5 hours without being accused of being creepy'
                
            },
            'Baseball Field' : {
              'north': 'Server Room',
              'west' : 'Server Room Two',
              'south': 'Mall',
              'codename' : 'windows',
              'challenge': 'Steve Ballmer throws a desk at you'  
            },
            'Server Room Two' : {
                'north' : 'Abandoned Building',
                'south' : 'Store',
                'east': 'Baseball Field',
                'codename': 'oracle',
                'challenge' : 'Larry Ellison tries to murder you'
            },
            'Store' : {
                'north' : 'Server Room Two',
                'east' : 'Mall',
                'codename': 'walmart',
                'challenge': 'you have to shop in a walmart for six hours'
            },
            'Mall' : {
                'north': 'Baseball Field',
                'west' : 'Store',
                'codename': 'dell',
                'challenge': 'you have to make a dell computer work'
            }
            
        }

# start the player in the Hall
currentLocation = 'Boat Dock'

showInstructions()

# breaking this while loop means the game is over
while True:
    showStatus()

    # the player MUST type something in
    # otherwise input will keep asking
    move = ''
    while move == '':  
        move = input('>')

    # normalizing input:
    # .lower() makes it lower case, .split() turns it to a list
    # therefore, "get golden key" becomes ["get", "golden key"]          
    move = move.lower().split(" ", 1)

    #if they type 'go' first
    if move[0] == 'go':
        #check that they are allowed wherever they want to go
        if move[1] in locations[currentLocation]:
            #set the current room to the new room
            currentLocation = locations[currentLocation][move[1]]
        # if they aren't allowed to go that way:
        else:
            print(purple)
            print('You cant go that way!')

    #if they type 'get' first
    if move[0] == 'take' :
        # make two checks:
        # 1. if the current room contains an item
        # 2. if the item in the room matches the item the player wishes to get
        if "codename" in locations[currentLocation] and move[1] in locations[currentLocation]['codename']:
            #add the item to their inventory
            challenges.append(move[1])
            #display a helpful message
            print(move[1] + ' challenge accepted')
            scrollTxt(locations[currentLocation]['challenge'])
            print(' \n ')
            fail()
            #delete the item key:value pair from the room's dictionary
            del locations[currentLocation]['codename']
        # if there's no item in the room or the item doesn't match
        else:
            #tell them they can't get it
            print(purple)
            print('Cant get ' + move[1] + '!')



    if fails >= 3:
        print(red)
        scrollTxt('You got to DIE \n')
        break

    if passes >= 5:
        print(green)
        scrollTxt('You win')
        print(yellow)
        scrollTxt('You win')
        print(purple)
        scrollTxt('You can leave now')
        
        break
