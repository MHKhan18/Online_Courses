'''
Created on Jan 8, 2019

@author: Mohammad Khan
'''
starting_annual_salary = int(input("Enter the starting annual salary:")) 

semi_annual_raise = .07
r = 0.04
total_cost = 1000000
down_payment = 0.25*total_cost 

month_limit = 36
epsilon = 100

current_savings =0
    
low = 0
high = 10000
portion_saved = (low+high)/2.0
guess_count = 0
is_possible = True

while   abs(current_savings - down_payment) > epsilon:
    
    #setting the mutating variables to initial state for each trial savings rate
    month = 0
    current_savings =0
    annual_salary = starting_annual_salary
    

    incremental = portion_saved/float(10000)#conversion to decimal points
    
    #current savings for the particular savings rate after 36 months 
    for i in range(1,month_limit+1):
        month+=1
        current_savings += ((current_savings * float(r)/12 ) + ((annual_salary/12)*(incremental)))
        if month >= 6 and month%6 ==0:
            annual_salary += (annual_salary * semi_annual_raise)
    
    if (current_savings-down_payment)<(-epsilon):
        low = portion_saved
        
    elif (current_savings-down_payment)>epsilon:
        high = portion_saved
    
    if high == low:
        is_possible = False
        break
    
    portion_saved = (low+high)/2.0
    guess_count += 1
        
  
if is_possible == True:     
    print("Best savings rate:"+ str(portion_saved/10000))
    print("Steps in bisection search: ", guess_count)
else:
    print("It is not possible to pay the down payment in three years.")
    
                
            


