number_input = int(input("Input an integer: "))
description = "positive number" if number_input > 0 else "negative number" if number_input < 0 else "zero"
print(f"Input number is {description}.")