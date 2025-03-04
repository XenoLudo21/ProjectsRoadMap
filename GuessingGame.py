import random
import threading
import time

highest_score = None
timer_expired = threading.Event()  # Event to signal when timer is expired
timer_thread = None

def introduction():
    print("Welcome to the number guessing game!")
    print("I am thinking of a number between 0 and 100... Can you guess my number?")
    print("You only have 5 chances, so... good luck!")
    print("Choose the difficulty: \n 1) Easy (10 chances) \n 2) Medium (5 chances) \n 3) Hard (3 chances)")

    try:
        lol = int(input("Enter your choice:"))
    except ValueError:
        print("Please enter a valid number for your choice (1, 2, 3)")
        return introduction()

    choice = {1: 10, 2: 5, 3: 3}.get(lol, 0)

    if choice == 0:
        print("Invalid choice! Restarting...")
        return introduction()

    print(f"Great! You've chosen level {lol}. You have {choice} attempts.")
    print("The 20-second timer has started!")
    game(choice)

def game(choice):
    global timer_expired, timer_thread

    li = list(range(0, 101))
    target = random.choice(li)
    attempts = 0

    timer_expired.clear()  # Reset the event before starting the timer
    timer_thread = threading.Thread(target=timer, args=(20,))
    timer_thread.start()  # Start the timer

    while attempts < choice and not timer_expired.is_set():
        try:
            guess = int(input("Enter your guess:"))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if guess == target:
            print("Good job! You've won! Your prize is... my deepest admiration!")
            update_highest_score(attempts)
            stop_game()
            loss()  # Call loss after game ends successfully
            return  # Exit the game function
        else:
            attempts += 1
            if guess < target:
                print("WRONG! The number is greater than " + str(guess))
            elif guess > target:
                print("WRONG! The number is less than " + str(guess))

    # If timer expired, check this condition:
    if timer_expired.is_set():
        print(f"❌ You've used all {choice} chances or finished time. The correct number was {target}.")
        stop_game()  # Ensure the game is stopped
        loss()  # Ask if they want to play again

def loss():
    again = input("Wanna play again? Yes/No").strip().lower()
    if again == "yes":
        introduction()  # Restart the game from introduction
    else:
        print("See you next time!")

def update_highest_score(attempts):
    global highest_score
    if highest_score is None:
        highest_score = attempts
    else:
        highest_score = min(highest_score, attempts)
    print(f"Your highest score is {highest_score} attempts!")

def timer(orol):
    global timer_expired
    while orol > 0 and not timer_expired.is_set():
        time.sleep(1)
        orol -= 1

    if not timer_expired.is_set():  # Timer expired
        print("⏳ Time's up!")
        timer_expired.set()  # Set the event to signal that time is up
        stop_game()  # Stop the game after time is up

def stop_game():
    # No need to join threads here, as the event will signal game over
    pass

def main():
    introduction()

if __name__ == "__main__":
    main()


