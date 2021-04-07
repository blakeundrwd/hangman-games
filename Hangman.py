'''
Description:
        You must create a Hangman game that allows the user to play and guess a secret word.  
        See the assignment description for details.
    
@author: Blake Underwood    beu2
'''
import random



def handleUserInputDifficulty():
    '''
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the 
    corresponding number of misses allowed for the game. 
    '''
    print("How many misses do you want? Hard has 8 and Easy has 12")
    diffi = input("(h)ard or (e)asy> ")
    if diffi == "e":
        print ("you have 12 misses to guess word")
        return 12 
    if diffi == "h":
        print ("you have 8 misses to guess word")
        return 8
    
    


def getWord(words, length):
    '''
    Selects the secret word that the user must guess. 
    This is done by randomly selecting a word from words that is of length length.
    '''
    secret = []
    for i in words:
        if len(i) == length:
            secret.append(i)
    secretWord = random.choice(secret)
    return secretWord
    



def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''
    lettersGuessed = sorted(lettersGuessed)
    line1 = "letters you've guessed: " + " ".join(lettersGuessed)
    line2 = "misses remaining = " + str(missesLeft)
    line3 = " ".join(hangmanWord)
    
    sep = ''.join(line1) + '\n' + ''.join(line2) + '\n' + ''.join(line3)
    displayString = ''.join(sep)
    return displayString




def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''
    
    print(displayString)
    x = True
    while x == True:
        letter = input("letters> ")
        print("\n")
        if letter not in lettersGuessed:
            lettersGuessed.append(letter)
            return letter    
        else:
            print("you already guessed that")
     


def updateHangmanWord(guessedLetter, secretWord, hangmanWord):
    '''
    Updates hangmanWord according to whether guessedLetter is in secretWord and where in secretWord guessedLetter is in.
    '''
    
    for x in range(len(secretWord)):
        if secretWord[x] == guessedLetter:
            hangmanWord[x] = guessedLetter
        else: hangmanWord = hangmanWord
    return hangmanWord




def processUserGuess(guessedLetter, secretWord, hangmanWord, missesLeft):
    '''
    Uses the information in the parameters to update the user's progress in the hangman game.
    '''
    progress = ['', missesLeft, True]
    progress[0] = updateHangmanWord(guessedLetter, secretWord, hangmanWord)
    if guessedLetter not in secretWord:
        progress[1] = missesLeft - 1
    if guessedLetter not in secretWord:
        progress[2] = False
    return progress
    
     


def runGame(filename):
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    '''

    f = open(filename) 
    words = f.readlines() 
    length = random.randint(5, 11)
    now = getWord(words, length)
    mode = handleUserInputDifficulty()
    missesLeft = 0
    idx = -1
    lettersGuessed = []
    hangmanWord = []
    hangmanWord1 = []
    words1 = [hangmanWord1]
    
    for h in range(len(now) - 1):
        hangmanWord.append("_")
        hangmanWord1.append("_")
    
    while True:
        display = createDisplayString(lettersGuessed, (mode - missesLeft), hangmanWord)
        letter = handleUserInputLetterGuess(lettersGuessed, display)
        updateWord = updateHangmanWord(letter, now, hangmanWord)
        words1.append(updateWord)
        idx += 1
        if words1[idx] != words1[idx + 1]:
            print(letter + " is in the word")
        else:
            print("you missed:", letter, "not in word")
            missesLeft += 1 
        words1.append(updateHangmanWord(letter, now, hangmanWord1))
        
        process = processUserGuess(letter, now, hangmanWord, mode - missesLeft)
        if "_" not in hangmanWord:
            print("You guessed the word: " + now)
            print("you made", len(lettersGuessed), "guesses with", missesLeft, "misses")
            print("\n")
            return True
        if mode - missesLeft <= 0:
            print("you're hung!")
            print("word is " + now)
            print("you made", len(lettersGuessed), "guesses with", missesLeft, "misses")
            print("\n")
            return False
    
        
    
if __name__ == "__main__":
    '''
    Running Hangman.py should start the game, which is done by calling runGame, therefore, we have provided you this code below.
    '''
    x = 0
    wins = 0
    losses = 0
    while True:
        run = runGame("lowerwords.txt")
        if run:
            wins += 1
        else:
            losses += 1
        playAgain = input("Would you like to play again (y or n)? ")
        if playAgain == "y":
            continue
        if playAgain == "n":
            print("Wins: ", wins, "Losses: ", losses)
            break
         
    
