###########################
# 6.0002 Problem Set 1b: Space Change
# Name: Mohammad Khan


#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    
    if (egg_weights,target_weight) in memo:
        result = memo[(egg_weights,target_weight)]
    
    elif target_weight == 0:
        result = 0
    
    elif len(egg_weights)==0 :
        result = float("inf") 
    
    elif egg_weights[0] > target_weight:
        result = dp_make_weight(egg_weights[1:],target_weight,memo)

    else:

        use_first = 1+dp_make_weight(egg_weights, target_weight - egg_weights[0], memo)
        lose_first = dp_make_weight(egg_weights[1:], target_weight, memo)

        result = min(use_first,lose_first)
    
    memo[(egg_weights,target_weight)] = result
    return result




# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()