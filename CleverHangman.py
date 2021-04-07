'''
Created on Nov 21, 2019

@author: Blake Underwood
'''

import random
import builtins
import operator

def handleUserInputDebugMode():
    '''
    Prompts user if they wish to play in DEBUG mode.
    '''
    type = input("Which mode do you want: (d)ebug or (p)lay: ")
    if type == "d":
        return True
    else:
        return False

def handleUserInputWordLength():
    '''
    Asks user how long the word should be.
    '''
    length = input("How many letters in the word you'll guess: ")
    if int(length) >= 5 or int(length) <= 10:
        return int(length)

def createTemplate(currTemplate, letterGuess, word):
    '''
    Creates a new template for the secret word that the user will see
    '''
    templatelist = list(currTemplate)
    words = list(word)
    for i in range(len(words)):
        if words[i] == letterGuess:
            templatelist[i] = letterGuess
    return "".join(templatelist)

def helperWord(words, length):
    '''
    Helper function that selects the secret word the user is trying to guess
    '''
    lst = []
    for i in words:
        if len(i) == length:
            lst.append(i)
    newword = random.randint(0, len(lst) - 1)
    return lst[newword]

def helperUpdateWord(guessedLetter, secretWord, hangmanWord):
    '''
    Helper function that updates hangman word based on wheter the guessed letter is in secret word.
    '''
    for i in range(len(hangmanWord)):
        if secretWord[i] == guessedLetter:
            hangmanWord[i] = guessedLetter
    return hangmanWord

def getNewWordList(currTemplate, letterGuess, wordList, DEBUG):
    '''
    creates a dictionary of strings as the key to lists as the value.
    '''
    dictStrings = {}
    for i in wordList:
        a = createTemplate(currTemplate, letterGuess, i)
        if a not in dictStrings:
            dictStrings[a] = []
        dictStrings[a].append(i)
    lst = sorted(dictStrings.items(), key = lambda x : x[0].count('_'))
    lst = sorted(lst, key = lambda x : len(x[1]))
    if DEBUG:
        for k,v in sorted(dictStrings.items()):
            print(k, ":", len(v))
        print("# keys =", str(len(dictStrings)))
    return lst[-1]

def processUserGuessClever(guessedLetter, hangmanWord, missesLeft):
    '''
    updates number of misses left and indicates wheter the user missed.
    '''
    correctGuess = False
    if guessedLetter not in hangmanWord:
        missesLeft -= 1
        correctGuess = False
    else:
        missesLeft = missesLeft
        correctGuess = True
    return [missesLeft, correctGuess]

def helperprocessUserGuessClever(guessedLetter, secretWord, hangmanWord, missesLeft):
    '''
    helper function that updates number of misses left, indicates wheter the user missed, and updates hangman word.
    '''
    correctGuess = False
    if guessedLetter not in secretWord:
        missesLeft -= 1
        correctGuess = False
    else:
        hangmanWord = helperUpdateWord(guessedLetter, secretWord, hangmanWord)
        correctGuess = True
    return [missesLeft, correctGuess]

def handleUserInputDifficulty():
    '''
    Asks user if they want to play in hard or easy mode.
    '''
    print("How many misses do you want? Hard has 8 and Easy has 12.")
    mode = input("(h)ard or (e)asy> ")
    if mode == "e":
        print("you have 12 misses to guess word\n")
        return 12
    if mode == "h":
        print("you have 8 misses to guess word\n")
        return 8

def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    '''
    creates a string that will be displayed to the user
    '''
    lettersNotGuessed = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    for i in range(len(lettersGuessed)):
        if lettersGuessed[i] in lettersNotGuessed:
            lettersNotGuessed[lettersNotGuessed.index(lettersGuessed[i])] = ' '
    p1 = "letters not yet guessed: ", ''.join(lettersNotGuessed)
    p2 = 'misses remaining = ', str(missesLeft)
    p3 = ' '.join(hangmanWord)
    display = ''.join(p1), '\n', ''.join(p2), '\n', ''.join(p3)
    displayString = ''.join(display)
    return displayString


def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    asks user to input a letter to guess and handles the input to check if in word or not.
    '''
    print(displayString)
    x = True
    while x == True:
        guessedLetter = input('letter> ')
        print('\n')
        if guessedLetter not in lettersGuessed:
            lettersGuessed.append(guessedLetter)
            return guessedLetter
        else:
            print('you already guessed that')

def runGame(filename):
    '''
    this function runs the entire clever hangman game.
    '''
    f = open(filename)
    wordList = f.read().split()
    words = []
    DEBUG = handleUserInputDebugMode()
    length = handleUserInputWordLength()
    misses = handleUserInputDifficulty()
    for word in wordList:
        if len(word) == length:
            words.append(word)
    secretWord = helperWord(words, length)
    hangmanWord = ["_"] * len(secretWord)
    newword = hangmanWord
    lettersGuessed = []
    missesleft = 0

    while ((misses - missesleft) > 0):
        display = createDisplayString(lettersGuessed, (misses - missesleft), hangmanWord)
        if DEBUG:
            display += "\n" + "(word is " + secretWord + ")" + "\n" + "# possible words: " + str(len(words))
        letter = handleUserInputLetterGuess(lettersGuessed, display)
        a = getNewWordList("".join(newword), letter, words, DEBUG)
        newword = a[0]
        words = a[1]
        secretWord = helperWord(words, length)

        pg = processUserGuessClever(letter, hangmanWord, (misses - missesleft))
        processGuess = helperprocessUserGuessClever(letter, secretWord, hangmanWord, (misses - missesleft))
        if processGuess[1]:
            print(letter, "is in the word!")
        else:
            print("you missed:", letter, "not in word \n")
            missesleft += 1
        if "_" not in hangmanWord:
            print("You guessed the word:", secretWord)
            print("you made", len(lettersGuessed), "guesses with", missesleft, "misses")
            print("\n")
            return True
        if (misses - missesleft) <= 0:
            print("you're hung!!")
            print("word is", secretWord)
            print("you made", len(lettersGuessed), "guesses with", missesleft, "misses")
            print("\n")
            return False


if __name__ == "__main__":
    '''
    the main block calls run game and runs the actual clever hangman game.
    '''
    x = True
    losses = 0
    wins = 0
    while x:
        run = runGame('lowerwords.txt')
        if run:
            wins += 1
        else:
            losses += 1
        another = input("Would you like to play again (y or n)? ")
        if another == 'y':
            continue
        else:
            print("Wins:", wins, "Losses:", losses)
            x = False