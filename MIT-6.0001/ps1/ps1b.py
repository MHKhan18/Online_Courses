'''
Created on Jan 8, 2019

@author: Mohammad Khan
'''
annual_salary = int(input("Enter your starting annual salary:"))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal:"))
total_cost = int(input("Enter the cost of your dream home:"))
semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal:"))

portion_down_payment = 0.25
current_savings = 0
r = 0.04 
month = 0

while   current_savings < (total_cost*portion_down_payment):
    month += 1
    current_savings += ((current_savings * float(r)/12 ) + ((annual_salary/12)*portion_saved))
    if month >= 6 and month%6 == 0:
        annual_salary += (annual_salary * semi_annual_raise)
    
    
print("Number of months:",month )
