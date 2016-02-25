# TYMEVENTURE v0.0.0
# Status: Basically nothing is here
# A simple curses-based game running i Python 3.4.3.
# Help would be appreciated if you know how.
#
# TODO:
# - Actually set up more than just 2 places
# - Make inventory more than just an empty list

import curses # Curses! You've foiled my plan!

inventory = list() # The player's inventory
gender = "neutral" # The player's gender, for him/her/they or he's/she's/they're

# The location class
class Location():
    def __init__(self, printName, desc):
        self.printName = printName # The "pretty" name it uses in the game
        self.desc = desc # The description it uses, which is what the player will see

        self.connections = list() # A list of all the places you can go to from this place
                                  # All elements in this are other Location() classes.
        self.itemsHere = list() # For another time

    def canGoTo(self, dest):
        ''' Can we go to the destination from here? '''
        return dest in self.connections

# Make a connection between two points.
def makeConnection(pointA, pointB):
    if not pointB in pointA.connections:
        pointA.connections.append(pointB)
        
    if not pointA in pointB.connections:
        pointB.connections.append(pointA)

# Small script I wrote a while back to get keypresses
def getKey(screen):
    return chr(screen.getch())

# Convienience function to quickly make menus like the intro
def nextMenu(screen):
    key = getKey(screen)
    screen.clear()
    screen.refresh()
    return key

yourHouse = Location("Your House", "Your house, the place you live in.")
outside = Location("Outside", "Outside your house. It sure looks scary. Perhaps you should stay on the internet.")

makeConnection(yourHouse, outside)


def main(stdscr):  
    currentLocation = yourHouse
    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr(0, 0, 'Welcome to Tymeventure! Press any key to continue.', curses.color_pair(0) | curses.A_BOLD)
    nextMenu(stdscr)

    stdscr.addstr(0, 0, "Let's get started. Are you a:", curses.color_pair(0) | curses.A_BOLD)
    stdscr.addstr(1, 0, "(b)oy", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(2, 0, "(g)irl", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(3, 0, "Or would you simply prefer not to share? (any other key)", curses.color_pair(0) | curses.A_BOLD)
    selection = nextMenu(stdscr).lower() # Ignore caps
    if selection == "b":
        gender = "boy"
    elif selection == "g":
        gender = "girl"
    else:
        gender = "neutral" # Simply say neutral, as they chose not to share.

    genderConfirm = "Got it, you chose " + gender + "."
    stdscr.addstr(0, 0, genderConfirm, curses.color_pair(0) | curses.A_BOLD)
    stdscr.addstr(1, 0, "What's your name? (max 24 characters)", curses.color_pair(0) | curses.A_BOLD)
    stdscr.addstr(2, 0, '> ', curses.color_pair(0) | curses.A_BOLD)
    playerName = stdscr.getstr(2, 2, 24).decode('utf8')
    stdscr.clear()
    stdscr.refresh()
    topbar = "OK " + playerName + ", you chose " + gender + " as your gender."
    stdscr.addstr(0, 0, topbar, curses.color_pair(0) | curses.A_BOLD)
    stdscr.addstr(1, 0, "Now get out there and do some adventuring!", curses.color_pair(0) | curses.A_BOLD)
    nextMenu(stdscr)

    continueGame = True
    while continueGame:
        topbar = playerName # May be expanded in the future
        stdscr.addstr(0, 0, topbar, curses.color_pair(0) | curses.A_BOLD)
        location = "Current Location: " + currentLocation.printName
        stdscr.addstr(1, 0, location, curses.color_pair(0) | curses.A_BOLD)
        description = currentLocation.desc
        stdscr.addstr(2, 0, description, curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(0, 40, "(Q)uit", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(1, 40, "(M)ove", curses.color_pair(0) | curses.A_BOLD)
        choice = getKey(stdscr).lower() # Case doesn't matter
        # Clear before we process so we can print
        stdscr.clear()
        stdscr.refresh()
        if choice == "q":
            continueGame = False
        elif choice == "m":
            ypos = 5
            stdscr.addstr(ypos - 1, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
            keycount = 1
            for place in currentLocation.connections:
                label = "|(" + str(keycount) + ")" + place.printName
                stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), curses.color_pair(0) | curses.A_BOLD)
                stdscr.addstr(ypos, 40, "|", curses.color_pair(0) | curses.A_BOLD) # Make a "box"
                ypos += 1
                keycount += 1
            stdscr.addstr(ypos, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
            stdscr.addstr(ypos + 1, 0, "Press the key next to where you want to move.", curses.color_pair(0) | curses.A_BOLD)
            choice = nextMenu(stdscr).lower() # Case doesn't matter
            if int(choice) - 1 < len(currentLocation.connections):
                moveTo = currentLocation.connections[int(choice) - 1]
                currentLocation = moveTo # Move us
        else:
            pass

        
if __name__=='__main__':
    try:
        stdscr = curses.initscr()
        curses.cbreak() # ; curses.noecho() # Uncomment if desired/needed
        curses.start_color()
        stdscr.keypad(1)
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)
        main(stdscr)                    # Enter the main loop
    except KeyboardInterrupt:
        pass # I may need something here later
    finally:
        stdscr.erase()
        stdscr.refresh()
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()                 # Terminate curses
