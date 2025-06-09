import random
import string

def select_random_word(word_list):
    return random.choice(word_list).upper()


def display_current_progress(secret_word, guessed_letters):
    return ' '.join([letter if letter in guessed_letters else '_' for letter in secret_word])


def play_hangman(word_list, max_incorrect=6):
    secret_word = select_random_word(word_list)
    guessed_letters = set()
    incorrect_guesses = 0

    print("Welcome to Hangman!")
    print(f"You have {max_incorrect} incorrect guesses allowed.")

    while True:
        print("\nWord:", display_current_progress(secret_word, guessed_letters))
        print(f"Incorrect guesses left: {max_incorrect - incorrect_guesses}")
        print(f"Guessed letters: {' '.join(sorted(guessed_letters))}")

        guess = input("Guess a letter: ").strip().upper()
        if len(guess) != 1 or guess not in string.ascii_uppercase:
            print("Please enter a single alphabet letter.")
            continue

        if guess in guessed_letters:
            print("You've already guessed that letter. Try again.")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"Good job! '{guess}' is in the word.")
        else:
            incorrect_guesses += 1
            print(f"Sorry, '{guess}' is not in the word.")

        if all(letter in guessed_letters for letter in secret_word):
            print(f"\nCongratulations! You guessed the word: {secret_word}")
            break

        if incorrect_guesses >= max_incorrect:
            print(f"\nGame over! The word was: {secret_word}")
            break


def main():
    # You can customize or load words from a file
    word_list = [
        'python', 'hangman', 'challenge', 'computer', 'programming',
        'interface', 'function', 'variable', 'condition', 'iteration'
    ]
    play_hangman(word_list)

if __name__ == '__main__':
    main()
