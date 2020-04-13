###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Mohammad Khan

from ps1_partition import get_partitions
import time
from pathlib import Path


#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    file_path = str( Path(__file__).resolve().parents[0] /filename ) 
    data_file = open(file_path,'r')
    cow_weight = {}

    for line in data_file: 
        data_pair = line.split(",") 
        weight = data_pair[1].rstrip() 
        
        cow_weight[data_pair[0]] = int(weight)
    
    data_file.close()

    return cow_weight

#print( load_cows("ps1_cow_data.txt") )



# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
   
    cows_by_weight = [ pair[0] for pair in sorted(cows.items(), key = lambda item:item[1], reverse=True) ] # sorts cows in descending order by weight and puts into list

    trips = []
    
    while  len(cows_by_weight) > 0:
        trip=[]
        total_weight = 0
        j = 0
        while j < len(cows_by_weight):
            cow = cows_by_weight[j]
            if total_weight + cows[cow] < limit:
                trip.append(cow)
                total_weight += cows[cow]
                cows_by_weight.remove(cow)
                j -= 1
            j+=1
        trips.append(trip)
       
    return trips 


#print(greedy_cow_transport(load_cows("greedy_test.txt")))

#for partition in get_partitions([1,2,3]):
#    print(partition)







    

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows_by_weight = [ pair[0] for pair in sorted(cows.items(), key = lambda item:item[1], reverse=True) ] # sorts cows in descending order by weight and puts into list
    
    for partition in get_partitions(cows_by_weight): # a partition is a list of lists
        invalid_combo = False
        for trip in partition: # a trip is a list of cows
            total_weight = 0
            for cow in trip:
                total_weight += cows[cow]
            if total_weight > limit:
                invalid_combo = True
                break
        
        if not invalid_combo:
            return partition 

#print(brute_force_cow_transport(load_cows("greedy_test.txt")))



        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    start = time.time()
    brute_force_sol = brute_force_cow_transport(load_cows("ps1_cow_data.txt"))
    end = time.time()
    brute_force_time = end - start

    start2 = time.time()
    greedy_sol = greedy_cow_transport(load_cows("ps1_cow_data.txt"))
    end2 = time.time()
    greedy_time = end2 - start2

    print( f'number of trips by brute force: {len(brute_force_sol)}')
    print( f'brute force time: {brute_force_time}')

    print( f'number of trips by greedy method: {len(greedy_sol)}')
    print( f'greedy method time: {greedy_time}')


compare_cow_transport_algorithms()
