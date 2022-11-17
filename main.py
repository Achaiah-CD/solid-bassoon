import random

# List of global constants.
MAX_LINES = 3
MAX_BET = 100   # Can only bet a max of $100 for each line.
MIN_BET = 1     # Min bet for each line.

# The slot dimensions.
ROWS = 3
COLS = 3

# Dict of Number of symbols each.
symbol_count = {
    "AA":2,
    "BB":4,
    "CC":6,
    "DD":8
}

# Dict of the multiplier if you win. (A - 5x.....)
symbol_value = {
    "AA":5,
    "BB":4,
    "CC":3,
    "DD":2
}


# Check if the transposed columns have rows of the same symbol.
def check_winnings(columns, lines, bet, values):

    winnings = 0
    winning_lines = []  # Lines that won.

    # To check only on the lines that have been bet.
    # Will not consider if the line is won but not bet by the user.
    for line in range(lines):
        symbol = columns[0][line]
        # As the column[0] contains the rows.
        # Use 'symbol' to compare

        for column in columns:
            symbol_to_check = column[line]
            # Checking in line'th element of each column in columns.
            if symbol != symbol_to_check:
                break

        # If the for loop has a break condition in it and it is not executed throughout, 
        # then the else will be called.
        # Here, if all symbols are same, else condition will be called.
        else:
            winnings += values[symbol] * bet
            # Bet * (the symbol multiplier)
            winning_lines.append(line+1)

    return winnings, winning_lines
    #Return how much has been won and on which lines.



# Select random symbols to appear in the machine.
def get_slot_machine_spin(rows,cols,symbols):
    all_symbols = []
    for symbol,symbol_count in symbols.items(): # items() returns key and value. 
        for _ in range(symbol_count):
            # Adding all the symbols individually to the all_symbols list.
            # Not preferred if the number of symbols and their frequency is high.
            all_symbols.append(symbol)

    columms = []
    # Will contain lists of columns in it.
    for _ in range(cols):
        column = []
        # Symbols in one column.

        # Copy to current_symbols.
        # current_symbols = all_symbols will just refer it to the original list, doesn't create a copy.
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        # Columns added in each loop
        columms.append(column)
        # Columns is now a transpose i.e., rows in place of colummns and vice-versa.
    return columms



# Prints after spinning the machine.
def print_slot_machines(columns):
    # Columns has the transpose of the actual matrix that should appear.
    print()

    # Print its transpose to get the correct display order.
    for row in range(len(columns[0])):
        for i,column in enumerate(columns): # Enumerate returns index(starting from 0) and element. 
            if i != len(columns)-1:
                print(column[row], end=" | ")
            else:
                print(column[row])  
    print()


# Main balance in user account.
def deposit():
    print()
    
    while True:
        amount = input("What would you like to deposit? $")
        # Check if the string contains a number
        # Returns true only for 0 and positive number. 
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.\n")
        else:
            print("Please enter a number.\n")

    return amount



# Gets the number of lines to bet on.
def get_number_of_lines():
    while True:
        lines = input("Enter the number of lines to bet on (1-"+str(MAX_LINES)+")? ")   #Convert to str as int wont be concatenated.
        # Check if the string contains a number
        # Returns true only for 0 and positive number. 
        if lines.isdigit():
            lines = int(lines)
            if 1<= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.\n")
        else:
            print("Please enter a number.\n")

    return lines



# Gets the bet for each line.
#The bet will be same for each line (for now).
def get_bet():
    while True:
        amount = input("What would you like to bet on each line? $")
        # Check if the string contains a number
        # Returns true only for 0 and positive number. 
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.\n")
        else:
            print("Please enter a number.\n")

    return amount



# Take lines, bet and spin.
def game(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"You do not have enough to bet that amount, your current balance is {balance}.\n")
        else:
            break
    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to ${total_bet}.")

    slots = get_slot_machine_spin(ROWS,COLS,symbol_count)
    print_slot_machines(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    
    # Print only if user won on any lines. i.e., list is not empty.
    if winning_lines:
        # *winning_lines (Here * is a splat operator. It unpacks all the lines won and prints with space)
        # If no lines were won it just prints nothing.
        print(f"You won on line number: ", *winning_lines,"\n")

    # Return the amount left after betting and winning/losing 
    return winnings-total_bet
    # If money was lost, returns negative to deduct from deposit.



# Get Deposit, play and leave
def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}.")
        print()
        if balance == 0:    #End game as user does not have any money.
            print("You're out of money!!\nThanks for playing.")
            break
        answer = input("Press enter to play(q to quit):  ")
        print()
        if answer == "q":
            break
        elif answer == "":  #Only play if "ENTER" has been pressed.
            balance += game(balance)
        else:               #Else loop back and ask again.
            print("Please enter 'ENTER' or 'q' only!!\n")

    #Leaving the game. The end!
    print(f"You left with ${balance}.\n\n")



# The entry point for the script
if __name__ == "__main__":
    main()