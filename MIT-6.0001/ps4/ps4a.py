# Problem Set 4A
# Name: Mohammad Khan

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    
   
        
    if len(sequence) == 1:
        return [sequence]
    else:  
        permutations = []
        apart_first_permutation = get_permutations(sequence[1:])
        for stn in apart_first_permutation:
            for i in range(len(stn)+1):
                new_stn = stn[0:i]+sequence[0]+stn[i:]
                permutations.append(new_stn)
    
        return permutations
    
    


#print(get_permutations('aeiou'))
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

 input1 = 'w'
 print('Input: ',input1)
 print('Expected Output: ', ['w'])
 print('Actual Output: ', get_permutations(input1))
 print('-'*13)
 
 input2 = 'us'
 print('Input: ',input2)
 print('Expected Output: ', ['us','su'])
 print('Actual Output: ', get_permutations(input2))
 print('-'*13)
 
 
 input3 = 'car'
 print('Input: ',input3)
 print('Expected Output: ', ['car','arc','rac','cra','acr','rca'])
 print('Actual Output: ', get_permutations(input3))
 
 
 
  
  
