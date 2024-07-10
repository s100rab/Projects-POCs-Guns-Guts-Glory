import os
import pickle

def add_word():
    word = input("Enter a word: ")
    meaning = input("Enter the meaning: ")
    words[word] = meaning
    save_words()

def find_meaning():
    word = input("Enter a word: ")
    if word in words:
        print(f"Meaning of '{word}': {words[word]}")
    else:
        print("Meaning not found.")

def update_word():
    word = input("Enter a word: ")
    if word in words:
        meaning = input("Enter the updated meaning: ")
        words[word] = meaning
        save_words()
    else:
        print("Word not found.")

def save_words():
    with open('words.txt', 'wb') as f:
        pickle.dump(words, f)

def load_words():
    if os.path.exists('words.txt'):
        with open('words.txt', 'rb') as f:
            return pickle.load(f)
    else:
        return {}

def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Add a new word")
        print("2. Find the meaning")
        print("3. Update a word")
        print("4. Exit")
        choice = int(input("Enter Choice: "))
        if choice == 1:
            add_word()
        elif choice == 2:
            find_meaning()
        elif choice == 3:
            update_word()
        elif choice == 4:
            break
        else:
            print("Invalid choice. Please try again.")

words = load_words()
main_menu()