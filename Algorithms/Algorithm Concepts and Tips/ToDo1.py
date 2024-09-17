# Setting and Swapping
# Set myNumber to 42. Set myName to your name. Now swap myNumber into myName & vice versa.


myNumber = 42
myName = 'Bayan'

swap = myNumber
myNumber = myName

myName = swap

print("swap my number to my name:" , myName)
print("swap my name to my number:" , myNumber)

# Print -52 to 1066
# Print integers from -52 to 1066 using a FOR loop.

for number in range(-52, 1067):
    print(number) 

# Don’t Worry, Be Happy
# Create beCheerful(). Within it, console.log string "good morning!" Call it 98 times.

def beCheerful():
    counter = 1
    while(counter < 99):
        print(counter , "good morning!")
        counter+=1
        
beCheerful()

# Multiples of Three – but Not All
# Using FOR, print multiples of 3 from -300 to 0. Skip -3 and -6.
def multiple():
    for multiple in range(-300, 1):
        if(multiple % 3 == 0 and (multiple != -3 and multiple != -6)):
            print(multiple)
                
multiple()   


# Printing Integers with While
# Print integers from 2000 to 5280, using a WHILE.

def printing_integers():
    number = 2000
    while(number <= 5280):
        print(number)
        number +=1
        
printing_integers()

# You Say It’s Your Birthday
# If 2 given numbers represent your birth month and day in either order, log "How did you know?", else log "Just another day...." 

def your_birthday(day, month):
    if( day == 1 and month == "March"):
        print("How did you know?")
    else:
        print("Just another day...." )            

day = int(input("Enter a Day: "))
month= str(input("Enter the name of the Month: "))

your_birthday(day, month)


        

