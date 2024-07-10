import os
import pickle

class EnglishDictionary:
    def __init__(self):
        self.words = {}
        self.file_name = 'words.txt'
        self.load_words()

    def load_words(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'rb') as f:
                self.words = pickle.load(f)

    def save_words(self):
        with open(self.file_name, 'wb') as f:
            pickle.dump(self.words, f)

    def add_word(self):
        word = input("Enter a word: ")
        meaning = input("Enter the meaning of the word: ")
        self.words[word] = meaning
        self.save_words()
        print("Word added successfully.")

    def find_meaning(self):
        word = input("Enter a word to find its meaning: ")
        if word in self.words:
            print(f"Meaning of '{word}': {self.words[word]}")
        else:
            print("Word not found.")
            #

    def update_word(self):
        word = input("Enter a word to update its meaning: ")
        if word in self.words:
            meaning = input("Enter the updated meaning of the word: ")
            self.words[word] = meaning
            self.save_words()
            print("Word updated successfully.")
        else:
            print("Word not found.")

    def run(self):
        while True:
            print("\nMain Menu")
            print("1. Add a new word")
            print("2. Find the meaning")
            print("3. Update a word")
            print("4. Exit")
            choice = int(input("Enter Choice: "))
            if choice == 1:
                self.add_word()
            elif choice == 2:
                self.find_meaning()
            elif choice == 3:
                self.update_word()
            elif choice == 4:
                print("Exiting the application.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = EnglishDictionary()
    app.run()