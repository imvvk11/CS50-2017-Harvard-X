

condition = False

while not condition:
    height = int(input("Height: "))   # prompt for a user input
    if height < 0 or height > 23:     # make condition for value of height should between 0 and 23.
        condition = True              # loop will break if height > 23 & height < 0.
    else:
        for i in range(1,height+1):   #use for loop to iterate and print height of pyramid
          print ((" ")*(height-i) + i * "#" + "  " + ((" ") + i * "#"))

        break


