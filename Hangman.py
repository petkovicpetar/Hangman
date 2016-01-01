#-------------------------------------------------------------------------------
# Name:        Hangman
# Purpose:     Project
# Author:      Petar Petkovic
# Copyright:   (c) ppetkovi@uwaterloo.ca 2015
#-------------------------------------------------------------------------------

from graphics import *
import time
import random

#This function creates the categories window and this is where the user choses
#which category they want
def welcome(win2):
    a=10
    b=5
    c=490
    d=75
    #Creating the category boxes and setting their colors to yellow
    for x in range(0,5):
        box1 = Rectangle(Point(a,b), Point(c,d))
        box1.setFill('yellow')
        box = box1.draw(win2)
        b+=80
        d+=80

    T1=240
    T2=40
    #Words in boxes, writes the words in the boxes(categories)
    words = ("FRUITS","COUNTRIES","CARS","SPORTS","COLOURS")
    word = ("Fruits.txt","Countries.txt","Cars.txt","Sports.txt","Colours.txt")
    for x in range(0,5):
        Category = Text(Point(T1,T2),words[x])
        Category.draw(win2)
        T2+=80

    b2,d2=0,0
    while True:
        p = win2.getMouse()
        if p.getX() >= 10 and p.getX() <= 490 and p.getY() >= 5 and p.getY() <= 75:
            x,b2,d2=0,5,75
        elif p.getX() >= 10 and p.getX() <= 490 and p.getY() >=85 and p.getY() <=155:
            x,b2,d2=1,85,155
        elif p.getX() >= 10 and p.getX() <= 490 and p.getY() >=165 and p.getY() <=235:
            x,b2,d2=2,165,235
        elif p.getX() >= 10 and p.getX() <= 490 and p.getY() >=245 and p.getY() <=315:
            x,b2,d2=3,245,315
        elif p.getX() >= 10 and p.getX() <= 490 and p.getY() >=325 and p.getY() <=395:
            x,b2,d2=4,325,395
        else:
            print("You need to press on a category")
        a=10
        c=490
        box2 = Rectangle(Point(a,b2), Point(c,d2))
        box2.setFill('green')
        Category = Text(Point(240,d2-35),words[x])
        box = box2.draw(win2)
        Category.draw(win2)
        time.sleep(0.5)
        win2.close()
        return word[x]

#This function creates the hangman person and frame where he will be hung from
def hangmanbody(win):
    #Creating the frame for the hangman
    topheadline = Line(Point(100,20), Point(100,70))
    topheadline.draw(win)
    topline = Line(Point(20,20), Point(100,20))
    topline.draw(win)
    sideline = Line(Point(20,20), Point(20,300))
    sideline.draw(win)
    bottomline = Line(Point(20,300), Point(100,300))
    bottomline.draw(win)

    #The head
    center = Point(100,100)
    circ = Circle(center, 30)
    circ.setFill('blue')

    #The eyes
    center = Point(90,90)
    lefteye = Circle(center, 5)
    lefteye.setFill('red')
    center = Point(110,90)
    righteye = Circle(center, 5)
    righteye.setFill('red')

    #rest of body
    mouthline = Line(Point(90,115), Point(110,120))
    bodyline = Line(Point(100,130), Point(100,220))
    lefthandline = Line(Point(100,160), Point(50,140))
    righthandline = Line(Point(100,160), Point(150,140))
    leftlegline = Line(Point(100,220), Point(50,250))
    rightlegline = Line(Point(100,220), Point(150,250))

    #Takes all the body parts, and puts them into a list which can be called on
    #from the main function when it is needed to be drawn on the window
    bodyparts = [circ,lefteye,righteye,mouthline,bodyline,lefthandline,righthandline,leftlegline,rightlegline]
    return bodyparts

#This is the keyboard function which draws the keyboard, and checks what letter the user
#guessed and if it's right displays it to the window and if it's wrong it shows
#a body part of the hangman.
def keyboard(win,length,word,win2,bodyparts):
    #This is to draw the rectangles for the buttons
    x = 12
    y = 330
    #To draw 26 rectangles. One for each letter
    for m in range(1,27):
        rect = Rectangle(Point(x,y), Point((x+23),y+23))
        rect.setFill('pink')
        box = rect.draw(win)
        #If the rectangle x value passes 480 pixels then start second row of letters
        x = x + 38
        if x >= 480:
            x = 12
            y = 370
    #This draws the letters in the middle of the boxes that we're drawn
    letters = ("abcdefghijklmnopqrstuvwxyz")
    z = 23
    q = 341
    w = 0
    #To draw 26 letters
    for n in range(1,27):
        letter = Text(Point(z,q),(letters[w]))
        letter.draw(win)
        z = z + 38
        w = w + 1
        #for second row of letters
        if w == 13:
            z = 23
            q = 381

    #Makes a box which will end up being a 'status box' telling the user to click
    #a letter, or if they've already clicked a letter
    chosen = Rectangle(Point(175,70), Point(475,110))
    chosen.setFill('beige')
    box = chosen.draw(win)

    #For lines drawn(lines for the letters ex. _ _ _ _ _), the x coordinates
    coordinates = []
    length = len(word)
    #Formula to find out where each x1, and x2 coordinates are
    point = (350 - (20*length + 10 * (length - 1))) / 2
    position = point + 160

    #This is so that all of the x coordinates of every line drawn can be appended
    #to one list, so it's in length of the word-1 since in the file "\n" is a space
    #so the space is being removed with the (-1)
    for i in range(length-1):
        xcoordinates = [position,position+20]
        coordinates.append(xcoordinates)
        position = position + 30

    #To get the word into a list with all the letters split
    word = word.lower()
    words = list(word)
    lengthofword = len(words)
    lastletter = lengthofword-1
    #Deletes the space which is there when the word is imported form the file
    del words[lastletter]

    #This pretty much does the engine of the program
    lettersguessed = []
    wordletters = []
    ycoordinate = 240
    count1 = 0
    count = 0
    correctguesses = 0
    #This is located in the middle of the 'status box' so that i can easily change
    #what the message in the box is dependant on where the user clicked
    text = Text(Point(325,90),"")
    text.draw(win)
    while count != 10:
        #This is so that if a user clicked a letter, and it was a double letter
        #that the count is correct and the difference is added
        if count1 > count:
            difference = count1 - count
            count = count + difference
        #If the control count is less than the actual count of letters guessed then
        #the user clicked a wrong letter so a body part is drawn
        elif count1 < count:
            bodyparts[count-1].draw(win)
            count1 = count
        #If the user has correct guesses same as the number of letters in the word
        #user wins
        elif correctguesses == length-1:
            #tells user they won, and changed the 'status bar' to green
            text.setText("YOU WIN!")
            chosen.setFill("Green")
            #new window pops-up and asks if they want to play again or quit
            win3 = GraphWin("Play Again or Quit?",200,100)
            playagain = Rectangle(Point(10,5), Point(190,45))
            playagain.setFill("yellow")
            playagain.draw(win3)
            playagaintext = Text(Point(100,25), "Play Again")
            playagaintext.draw(win3)
            quitgame = Rectangle(Point(10,55), Point(190,95))
            quitgame.setFill("yellow")
            quitgame.draw(win3)
            quitgametext = Text(Point(100,75), "Quit")
            quitgametext.draw(win3)
            #Waits for a click on either play again or quit, if they press quit then
            #everything closes, if they press play again then hangman starts again
            #from the begining
            while True:
                p = win3.getMouse()
                if p.getX() >= 10 and p.getX() <= 190 and p.getY() >=5 and p.getY() <=45:
                    playagain.setFill("green")
                    time.sleep(.5)
                    win3.close()
                    win2.close()
                    win.close()
                    hangman()
                elif p.getX() >= 10 and p.getX() <= 190 and p.getY() >=55 and p.getY() <=95:
                    quitgame.setFill("red")
                else:
                    print("You need to chose either 'Play Again', or 'Quit'")
                time.sleep(.5)
                win3.close()
                win2.close()
                win.close()
        #If the count gets to 9(meaning that all the body parts have been drawn) then
        #the player loses
        elif count == 9:
            #The 'status bar' says you lose, and turns red
            text.setText("YOU LOSE!")
            chosen.setFill("red")
            #New window pops up asking if the user wants to quit or play again
            win3 = GraphWin("Play Again or Quit?",200,100)
            playagain = Rectangle(Point(10,5), Point(190,45))
            playagain.setFill("yellow")
            playagain.draw(win3)
            playagaintext = Text(Point(100,25), "Play Again")
            playagaintext.draw(win3)
            quitgame = Rectangle(Point(10,55), Point(190,95))
            quitgame.setFill("yellow")
            quitgame.draw(win3)
            quitgametext = Text(Point(100,75), "Quit")
            quitgametext.draw(win3)
            #Waits for a click on either play again or quit, if they press quit then
            #everything closes, if they press play again then hangman starts again
            #from the begining
            while True:
                p = win3.getMouse()
                if p.getX() >= 10 and p.getX() <= 190 and p.getY() >=5 and p.getY() <=45:
                    playagain.setFill("green")
                    time.sleep(.5)
                    win3.close()
                    win2.close()
                    win.close()
                    hangman()
                elif p.getX() >= 10 and p.getX() <= 190 and p.getY() >=55 and p.getY() <=95:
                    quitgame.setFill("red")
                    time.sleep(.5)
                    win3.close()
                    win2.close()
                    win.close()
                else:
                    print("You need to chose either 'Play Again', or 'Quit'")
        #If the player doesn't win, or lose then it goes here where it has them
        #click and chose a letter to be guessed.
        else:
            clicked = False
            a,b,c,d,e,f,g=12,35,330,353,23,341,0
            p = win.getMouse()
            for x in range(0,26):
                #if it hits letter 13 needs to move to second row of letters
                if x == 13:
                    a,b,c,d,e,f=12,35,370,393,23,381
                if p.getX() >= a and p.getX() <= b and p.getY() >=c and p.getY() <=d:
                    #makes letter grey once it's been clicked
                    rect = Rectangle(Point(a,c), Point((b),d))
                    rect.setFill('grey')
                    box = rect.draw(win)
                    letter = Text(Point(e,f),(letters[g]))
                    letter.draw(win)
                    guessedletter = (letters[g])
                    clicked = True
                    #if letter has already been clicked it shows that in the status box
                    if guessedletter in lettersguessed:
                        text.setText("Letter a has been clicked")
                    else:
                        for l in range (len(words)):
                            if guessedletter == words[l]:
                                #if the letter is in the word calculates the position it should be displayed at
                                xcoordinate = ((coordinates[l][1] - coordinates[l][0]) // 2) + coordinates[l][0]
                                letter = Text(Point(xcoordinate,ycoordinate),words[l])
                                letter.draw(win)
                                correctguesses = correctguesses + 1
                                count = count - 1
                        count = count + 1
                        text.setText("")
                        lettersguessed.append(guessedletter)
                a+=38
                b+=38
                e+=38
                g+=1
            #if no letter is clicked means that white space has been clicked and shows message
            if clicked == False:
                text.setText("Please click on a letter!")

#This draws the legend in the window so the user knows what letters have been guessed
#and what letters havent (pink = not guessed ... grey = already guessed)
def legend(win):
    greybox = Rectangle(Point(310,20), Point((330),40))
    greybox.setFill('grey')
    greybox.draw(win)
    pinkbox = Rectangle(Point(460,20), Point((480),40))
    pinkbox.setFill('pink')
    pinkbox.draw(win)
    guessed = Text(Point(235,30),"Already Guessed:")
    guessed.draw(win)
    notguessed= Text(Point(400,30),"Not Guessed:")
    notguessed.draw(win)

#This is the main function which calls on the other functions
def hangman():
    #error check, to see if the user pressed x or not and to make sure the user
    #safely exits the window without errors
    try:
        #This is the category window
        win2 = GraphWin("Choose a category:",500,400)
        Category = welcome(win2)
        length = len(Category)

        Categories = (Category[:-4])
        #The main window with the game
        win = GraphWin(("Hangman:" ,Categories,),500,400)

        #this choses a random word from the category that the user chose
        infile = open(Category,"r")
        file = infile.readlines()
        number = random.randint(1,100)
        word = file[number-1]
        word.lower()
        length = len(word)

        #formula to calculate how much space there is to plot each line for all
        #of the letters in the word (ex. _ _ _ _ _ _)
        point = (350 - (20*length + 10 * (length - 1))) / 2
        position = point + 160

        #this is to display a line for each letter in the word to the main window
        for i in range(length-1):
            line = Line(Point(position,250), Point(position+20,250))
            line.draw(win)
            position = position + 30

        #Calls upon the legend so it is displayed in the main window of the game
        legend(win)
        #Calls upon the keyboard function which has the main engine of the game in it
        keyboard(win,length,word,win2,hangmanbody(win))
    #Closes the window without an error
    except GraphicsError:
        print("Program Terminated.")
hangman()