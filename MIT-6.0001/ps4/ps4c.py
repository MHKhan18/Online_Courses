# Problem Set 4C
# Name: Mohammad Khan

import string
from ps4a import get_permutations
from pathlib import Path

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    file_name = str( Path(__file__).resolve().parents[0] / file_name ) 
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.__message_text = text 
        self.__valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.__message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.__valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
       
        dct = {}
        
        for i in range(len(VOWELS_LOWER)):
            dct[VOWELS_LOWER[i]] = vowels_permutation.lower()[i]
        
        for i in range(len(VOWELS_UPPER)):
            dct[VOWELS_UPPER[i]] = vowels_permutation.upper()[i]
            
        for i in range(len(CONSONANTS_LOWER)):
            dct[CONSONANTS_LOWER[i]] = CONSONANTS_LOWER[i]
            
        for i in range(len(CONSONANTS_UPPER)):
            dct[CONSONANTS_UPPER[i]] = CONSONANTS_UPPER[i]
            
        return dct
            
            
        
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        encrypt_txt = ''
        for word in self.__message_text.split(' '):
            new_word = ''
            for letter in word:
                if letter in string.ascii_letters:
                    new_word += transpose_dict[letter]
                else:
                    new_word += letter 
            encrypt_txt += new_word + ' '
        
        return encrypt_txt
    




class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)
        self.__valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        self.__perm_wrd = {}
        for permutation in get_permutations(VOWELS_LOWER):
            #print(permutation)
            #print(self.__perm_wrd)
            num_matches = 0
            for word in (self.apply_transpose(self.build_transpose_dict(permutation))).split(' '):
                #print(word)
                if is_word(self.__valid_words, word):
                    num_matches += 1
            self.__perm_wrd[permutation] = num_matches 
         
        #print(self.__perm_wrd)   
            
        matches_perm = max(zip(self.__perm_wrd.values(),self.__perm_wrd.keys()))
        
        word_matches , mutation = matches_perm
        
        if word_matches >= 1:
            return self.apply_transpose(self.build_transpose_dict(mutation))
        return self.__message_text  
            
                
            
if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    print('-'*13)
    #TODO: WRITE YOUR TEST CASES HERE
    message2 = SubMessage("Once Again?")
    permutation = 'aioeu'
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message2.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Enci Agaon?")
    print("Actual encryption:", message2.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message2.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    print('-'*13)
    
    message3 = SubMessage("Now, then")
    permutation = 'ioeua'
    enc_dict = message3.build_transpose_dict(permutation)
    print("Original message:", message3.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Nuw, thon")
    print("Actual encryption:", message3.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message3.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    print('-'*13)
    
