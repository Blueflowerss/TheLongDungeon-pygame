a = input("a -->")
b = input("b -->")

#y = ax + b
for x in range(-5,5):
    if a != "" and b != "":
        tempA = float(a) * x
        print("y = "+str(tempA)+"x + "+str(b))
    else:
        print("input numbers.")