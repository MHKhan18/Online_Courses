# Problem Set 2, hangman.py
# Name: Mohammad Khan


# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
from pathlib import Path


WORDLIST_FILENAME = str( Path(__file__).resolve().parents[0] /"words.txt ") 

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
        if letter not in letters_guessed:
            return False 
        
    return True 
#===============================================================================
# secret_word = 'apple'  
# letters_guessed = ['e', 'i', 'k', 'p', 'r', 's']
# print(is_word_guessed(secret_word, letters_guessed) )
#===============================================================================


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word_lst = ['_ ']*len(secret_word)
    for i in range(len(secret_word)):
        if secret_word[i] in letters_guessed:
            guessed_word_lst[i] = secret_word[i]
            
    guessed_word_str = ''
    for elem in guessed_word_lst:
        guessed_word_str += elem
    
    return guessed_word_str
            
    

#===============================================================================
# secret_word = 'apple'
# letters_guessed = ['e', 'i', 'k', 'p', 'r', 's']
# print(get_guessed_word(secret_word, letters_guessed))
#===============================================================================







#print(string.ascii_lowercase )


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    avaiable_letters = ''
    for letter in string.ascii_lowercase :
        if letter not in letters_guessed:
            avaiable_letters += letter
    
    return avaiable_letters
            
            
#===============================================================================
# letters_guessed = ['e', 'i', 'k', 'p', 'r', 's']
# print( get_available_letters(letters_guessed))
#             
#         
#     
#===============================================================================
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    
    guesses = 6
    warnings = 3
    print("You have " + str(warnings) + " warnings left")
    print("_ "*13)
    letters_guessed = [ ]
    
    while guesses>0 and is_word_guessed(secret_word, letters_guessed)==False :
        
        
        print("You have " + str(guesses) + " guesses left")
        print("Available letters: " + get_available_letters(letters_guessed)  )
        user_input = input("Please guess a letter:")
        if str.isalpha(str.lower(user_input)) and user_input not in letters_guessed:
            letters_guessed.append(user_input)
            if user_input in secret_word:
                print("Good guess:" + get_guessed_word(secret_word, letters_guessed) )
                
            else:
                print("Oops! That letter is not in my word:" + get_guessed_word(secret_word, letters_guessed))
                if user_input in ['a','e','i','o','u']:
                    guesses -= 2
                else:
                    guesses-=1
            print("_ "*13)
        else:
            if warnings<1:
                guesses-=1
            warnings-=1
            if str.isalpha(str.lower(user_input)) == False:
                print("Oops! That is not a valid letter. ",end=" ")
                if warnings>=0:
                    print("You have "  + str(warnings) +  " warnings left: " + get_guessed_word(secret_word, letters_guessed) ) 
                if warnings<0:
                    print("You have no warnings left so you lose one guess:" + get_guessed_word(secret_word, letters_guessed) )
                    
            if user_input in letters_guessed:
                print("Oops! You've already guessed that letter. ", end=" ")
                if warnings>=0:
                    print("You have "  + str(warnings) +  " warnings left: " + get_guessed_word(secret_word, letters_guessed) ) 
                if warnings<0:
                    print("You have no warnings left so you lose one guess:" + get_guessed_word(secret_word, letters_guessed) )  
            print("_ "*13)
        
                
        
        
    def unique_letters_counter(secret_word):
        ref = [secret_word[0]]
        unique_letters = 1
        
        for letter in secret_word:
            if letter not in ref:
                unique_letters += 1
                ref.append(letter)
        
        return unique_letters 
    
    if is_word_guessed(secret_word, letters_guessed) == True:
        print("Congratulations, you won!")
        total_score = guesses * unique_letters_counter(secret_word)
        print("Your total score for this game is: ", total_score)
    
    if guesses<=0:
        print("Sorry, you ran out of guesses. The word was " + secret_word)
        
                
                
            


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace(" ","")
    
    
    other_word = other_word.strip()
    
    if len(my_word) != len(other_word):
        return False
    
    for i in range(len(my_word)):
        if other_word[i] in my_word and my_word[i] != other_word[i]:
            return False
        if my_word[i] == '_':
            continue
        if my_word[i] != other_word[i]:
            return False 
    return True 
#print(len("a_ _ le"))
#===============================================================================
# print(match_with_gaps("te_ t", "tact"))
# print(match_with_gaps("a_ _ le", "banana"))
# print(match_with_gaps("a_ _ le", "apple"))
# print(match_with_gaps("a_ ple", "apple"))
#===============================================================================

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
  
    
    matches = False 
    for other_word in wordlist:
        if match_with_gaps(my_word, other_word):
            matches = True 
            print(other_word ,end=" ")
    print()
    if matches == False:    
        print("No matches found")
        
            
#===============================================================================
# show_possible_matches("t_ _ t")
# show_possible_matches("abbbb_ ")
# show_possible_matches("a_ pl_ ")
#===============================================================================


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
   
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    
    guesses = 6
    warnings = 3
    print("You have " + str(warnings) + " warnings left")
    print("_ "*13)
    letters_guessed = [ ]
    
    
    while guesses>0 and is_word_guessed(secret_word, letters_guessed)==False :
        
        print("You have " + str(guesses) + " guesses left")
        print("Available letters: " + get_available_letters(letters_guessed)  )
        user_input = input("Please guess a letter:")
        if user_input == "*":
            print("Possible word matches are:")
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            print("_ "*13)
            continue
            
        if str.isalpha(str.lower(user_input)) and user_input not in letters_guessed:
            letters_guessed.append(user_input)
            if user_input in secret_word:
                print("Good guess:" + get_guessed_word(secret_word, letters_guessed) )
                
            else:
                print("Oops! That letter is not in my word:" + get_guessed_word(secret_word, letters_guessed))
                if user_input in ['a','e','i','o','u']:
                    guesses -= 2
                else:
                    guesses-=1
            print("_ "*13)
        else:
            if warnings<1:
                guesses-=1
            warnings-=1
            if str.isalpha(str.lower(user_input)) == False:
                print("Oops! That is not a valid letter. ",end=" ")
                if warnings>=0:
                    print("You have "  + str(warnings) +  " warnings left: " + get_guessed_word(secret_word, letters_guessed) ) 
                if warnings<0:
                    print("You have no warnings left so you lose one guess:" + get_guessed_word(secret_word, letters_guessed) )
                    
            if user_input in letters_guessed:
                print("Oops! You've already guessed that letter. ", end=" ")
                if warnings>=0:
                    print("You have "  + str(warnings) +  " warnings left: " + get_guessed_word(secret_word, letters_guessed) ) 
                if warnings<0:
                    print("You have no warnings left so you lose one guess:" + get_guessed_word(secret_word, letters_guessed) )  
            print("_ "*13)
        
                
        
        
    def unique_letters_counter(secret_word):
        ref = [secret_word[0]]
        unique_letters = 1
        
        for letter in secret_word:
            if letter not in ref:
                unique_letters += 1
                ref.append(letter)
        
        return unique_letters 
    
    if is_word_guessed(secret_word, letters_guessed) == True:
        print("Congratulations, you won!")
        total_score = guesses * unique_letters_counter(secret_word)
        print("Your total score for this game is: ", total_score)
    
    if guesses<=0:
        print("Sorry, you ran out of guesses. The word was " + secret_word)
        
                
                




if __name__ == "__main__":
    
    #secret_word = choose_word(wordlist)
    #secret_word = "apple"
    #hangman(secret_word)
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
