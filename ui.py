# Importing necessary modules
from tkinter import *
from flashcard import *
import random
from tkinter import messagebox as mb
import csv
import pandas as pd
# Setting background color

BACKGROUND_COLOR = "pink"

# Defining the main class for the Flashcard Interface
class FlashcardInterface:
    def __init__(self, flashcard_brain):
        
        # Start the flashcard brain object
        self.flashcard = flashcard_brain
        # Creating the main window
        self.window = Tk()
        self.window.title("Flashy")
        self.window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
        self.window.geometry("1170x900")

        # Loading images for different elements
        self.card_front_img = PhotoImage(file="images/card_front.png")
        self.card_back_img = PhotoImage(file="images/card_back.png")
        self.study_me_img = PhotoImage(file="images/Me1.png")
        self.check_image = PhotoImage(file="images/right.png")
        self.flip_image = PhotoImage(file="images/flip.png")
        self.cross_image = PhotoImage(file="images/wrong.png")
        self.start_img = PhotoImage(file="images/start.png")
        self.create_img = PhotoImage(file="images/create.png")
        self.about_img = PhotoImage(file="images/about.png")
        self.quit_img = PhotoImage(file="images/quit.png")
        self.back_img = PhotoImage(file="images/back.png")
        self.add_img = PhotoImage(file="images/add.png")
        
        # Setting up the initial front page
        self.front_page_start()
        # Starting the main loop
        self.window.mainloop()
        
     # Function to display the next flashcard   
    def next_card(self):
        try:
             # Selecting a random card from the list of cards to learn
            self.flashcard.current_card = random.choice(self.flashcard.to_learn)
             # Updating canvas elements to display the question side of the flashcard
            self.canvas_2.itemconfig(self.card_title, text="Question", fill="black")
            self.canvas_2.itemconfig(self.card_word, text=self.flashcard.current_card["Question"], fill="black")
            self.canvas_2.itemconfig(self.card_background, image=self.card_front_img)
        except IndexError:
            # If there are no more cards to learn, display a message
            mb.showinfo("Out of questions", "Congratulations! You have learned all of the questions!")
            self.back()

    # Function to flip the flashcard
    def flip_button_func(self):
         # Defining states for the flip button (question side and answer side)
        flip_states = {
            0: {"title": "Question", "word_fill": "black", "background_image": self.card_front_img},
            1: {"title": "Answer", "word_fill": "white", "background_image": self.card_back_img}
        }
        current_state = flip_states[self.flashcard.flip_counter % 2]
        
        # Updating canvas elements to display the flipped side of the flashcard
        self.canvas_2.itemconfig(self.card_title, text=current_state["title"], fill=current_state["word_fill"])
        self.canvas_2.itemconfig(self.card_word, text=self.flashcard.current_card[current_state["title"]],
                                  fill=current_state["word_fill"])
        self.canvas_2.itemconfig(self.card_background, image=current_state["background_image"])

        # Incrementing flip counter
        self.flashcard.flip_counter += 1
    
    # Function to add new flashcards
    def add(self): 
        # Getting input from entry widgets for question and answer
        question = [q.get() for q in self.flashcard.q_entry if len(q.get()) != 0]
        answer = [a.get() for a in self.flashcard.a_entry if len(a.get()) != 0]

        # Checking if number of questions and answers match
        if not len(question) == len(answer):
            mb.showerror("Uneven question and answer", "Please input all the questions and answers")
        else:
            # Creating a dictionary of questions and answers
            q_and_a = {k: v for (k, v) in zip(question, answer)}
            # Converting the dictionary to a DataFrame
            df = ps.DataFrame(list(q_and_a.items()), columns=['Question', 'Answer'])

            # Update the existing CSV file
            csv_file_path = 'data/questions_and_answers.csv'
            try:
                existing_df = ps.read_csv(csv_file_path)
                updated_df = ps.concat([existing_df, df], ignore_index=True)
                updated_df.to_csv(csv_file_path, index=False)

                # Update the to_learn variable
                self.to_learn = updated_df.to_dict(orient="records")
            except FileNotFoundError:
                with open('data/questions_and_answers.csv', 'w', newline='') as csvfile:
                    fieldnames = ['Question', 'Answer']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for key in q_and_a:
                        writer.writerow({'Question': key, 'Answer': q_and_a[key]})
                data = ps.read_csv("data/questions_and_answers.csv")
                self.to_learn = data.to_dict(orient="records")

            mb.showinfo("Question updated", "Questions and Answers have been updated successfully")
            self.clear_entries()
        
    # Function to clear entry widgets
    def clear_entries(self):
        for entry in self.flashcard.q_entry + self.flashcard.a_entry:
            entry.delete(0, END)
            
    # Function to initialize the create flashcard interface
    def init_create(self):
        self.back_frame = Frame(self.window, bg=BACKGROUND_COLOR)
        self.back_frame.grid(row=0, column=0, columnspan=3)
        self.canvas_3 = Canvas(self.back_frame, width=1000, height=700)
        self.card_background = self.canvas_3.create_image(500, 300, image=self.card_front_img)

        
        self.canvas_3.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas_3.grid(row=0, column=0, columnspan=3)

        self.add_button = Button(image=self.add_img, highlightthickness=0, command=self.add)
        self.add_button.place(x=300, y= 650)

        self.back_button = Button(self.back_frame, image=self.back_img, highlightthickness=0, command=self.back)
        self.back_button.place(x=0, y=0)
        for i in range(5):
            self.q_text_box = Entry(self.window)  # create a new textbox
            self.q_text_box.place(x=160, y=75+(i*100), width=300, height=40)
            self.flashcard.q_entry.append(self.q_text_box)

            self.a_text_box = Entry(self.window)  # create a new textbox
            self.a_text_box.place(x=660, y=75+(i*100), width=300, height=40)
            self.flashcard.a_entry.append(self.a_text_box)

            self.q_label = Label(self.back_frame, text=f"Q{i+1}", font=("Ariel", 40, "italic"), bg="white")
            self.q_label.place(x=75, y=65+(i*100))

            self.a_label = Label(self.back_frame, text=f"A{i+1}", font=("Ariel", 40, "italic"), bg="white")
            self.a_label.place(x=575, y=65+(i*100))

    # Function to display the front page
    
    def front_page_start(self):
        global front_frame, card_background, study_buddy_logo, card_title, card_word
        self.front_frame = Frame(self.window, bg=BACKGROUND_COLOR)
        self.front_frame.grid(row=0, column=0, columnspan=3)
        self.canvas = Canvas(self.front_frame, width=1066, height=701)

        self.start_button = Button(self.front_frame, image=self.start_img, highlightthickness=0, command=self.start)
        self.start_button.place(x=480, y=250)

        self.create_button = Button(self.front_frame, image=self.create_img, highlightthickness=0, command=self.create)
        self.create_button.place(x=480, y=350)

        self.about_button = Button(self.front_frame, image=self.about_img, highlightthickness=0)
        self.about_button.place(x=480, y=450)
    

        self.quit_button = Button(self.front_frame, image=self.quit_img, highlightthickness=0, command=self.window.destroy)
        self.quit_button.place(x=480, y=550)
        self.card_background = self.canvas.create_image(533, 350, image=self.card_front_img)
        self.study_me_logo = self.canvas.create_image(533, 150, image=self.study_me_img)
        self.card_title = self.canvas.create_text(533, 150, text="", font=("Ariel", 40, "italic"))
        self.card_word = self.canvas.create_text(430, 350, text="", font=("Ariel", 40, "bold")) 
        self.canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=3)
        
    
    def init_start(self):
        global card_background, card_title, card_word, canvas_2, back_frame
        self.back_frame = Frame(self.window, bg=BACKGROUND_COLOR)
        self.back_frame.grid(row=0, column=0, columnspan=3)
        self.canvas_2 = Canvas(self.back_frame, width=1050, height=630)

        self.card_background = self.canvas_2.create_image(500, 300, image=self.card_front_img)
        self.card_title = self.canvas_2.create_text(533, 150, text="", font=("Ariel",17, "italic"))
        self.card_word = self.canvas_2.create_text(533, 350, text="", font=("Ariel",17,"bold"))
        self.canvas_2.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas_2.grid(row=0, column=0, columnspan=3)

        self.unknown_button = Button(self.back_frame, image=self.cross_image, highlightthickness=0, command=self.next_card)
        self.unknown_button.grid(row=1, column=0)

        self.flip_button = Button(self.back_frame, image=self.flip_image, highlightthickness=0, command=self.flip_button_func)
        self.flip_button.grid(row=1, column=2)
    

        self.known_button = Button(self.back_frame, image=self.check_image, highlightthickness=0, command=self.is_known)
        self.known_button.grid(row=1, column=1)

        self.back_button = Button(image=self.back_img, highlightthickness=0, command=self.back)
        self.back_button.place(x=0, y=0)

        self.next_card()

    #Function to start studying flashcards
    def start(self):
        self.flashcard.check_data()
        self.front_frame.destroy()
        try:
            random.choice(self.flashcard.to_learn)
        except IndexError:
            mb.showerror("Error", "No cards to study")
            self.front_page_start()
        else:
            self.init_start()

    # Function to create new flashcards
    def create(self):
        self.front_frame.destroy()
        self.init_create()

     #Function to navigate back to previous interfaces
    def back(self):
        try:
            self.add_button.destroy()
        except Exception:
            self.back_frame.destroy()
            self.front_page_start()
        else:
            self.back_frame.destroy()
            self.front_page_start()
    # Function to mark a flashcard as known
    def is_known(self):
        self.flashcard.is_known()
        self.next_card()
        
    
