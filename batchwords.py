from Tkinter import *
import tkFileDialog
import os

class MainWindow:

    def __init__(self, master):

        self.csv_directory = None       # the absolute path of the directory chosen
        self.all_csv_files = []         # all file names under the csv_directory
        self.selected_csv_files = []    # integers representing the index of files chosen (from self.all_csv_files)

        self.word_list_file = None
        self.word_list = None

        self.root = master
        self.root.title("Batch Words")
        self.root.geometry("800x500")
        self.main_frame = Frame(root)
        self.main_frame.pack()

        self.av_int_var = IntVar()

        self.video_selected_button = Radiobutton(self.main_frame,
                                                 text="video",
                                                 variable=self.av_int_var,
                                                 value=1)

        self.audio_selected_button = Radiobutton(self.main_frame,
                                                 text="audio",
                                                 variable=self.av_int_var,
                                                 value=2)

        self.video_selected_button.grid(row=3, column=3)
        self.audio_selected_button.grid(row=3, column=4)


        self.file_listbox_label = Label(self.main_frame, text="Files")
        self.file_listbox_label.grid(row=0, column=0)



        self.file_listbox = Listbox(self.main_frame,
                                    width=22,
                                    height=20,
                                    selectmode=MULTIPLE)

        self.file_listbox.grid(row=1, column=0, padx=10)




        self.file_list_load_button = Button(self.main_frame,
                                            text="Load",
                                            command=self.directory_load)

        self.file_list_load_button.grid(row=2, column=0)




        self.file_select_button = Button(self.main_frame,
                                         text="Select",
                                         command=self.select_files)

        self.file_select_button.grid(row=3, column=0)



        self.file_list_clear_button = Button(self.main_frame,
                                             text="Clear",
                                             command=self.directory_clear)

        self.file_list_clear_button.grid(row=4, column=0)


        self.wordlist_label = Label(self.main_frame, text="Word List")
        self.wordlist_label.grid(row=0, column=1)

        self.wordlist_box = Listbox(self.main_frame,
                                    width=22,
                                    height=20)

        self.wordlist_box.grid(row=1, column=1)


        self.load_wordlist_button = Button(self.main_frame,
                                           text="Load Word List",
                                           command=self.load_wordlist)

        self.load_wordlist_button.grid(row=2, column=1)


        self.export_csv = Button(self.main_frame, text="Export", command=self.export_csv)
        self.export_csv.grid(row=2, column=3, columnspan=2)

    def directory_load(self):

        self.directory_clear()

        self.csv_directory = tkFileDialog.askdirectory()

        for subdir, dirs, files in os.walk(self.csv_directory):
            for file in files:
                self.all_csv_files.append(file)
                #print os.path.join(subdir, file)
                print self.all_csv_files

        for i, file in enumerate(self.all_csv_files):
            self.file_listbox.insert(i, file)

    def directory_clear(self):

        self.all_csv_files = []
        self.selected_csv_files = []

        self.file_listbox.delete(0, END)

    def select_files(self):

        print self.file_listbox.curselection()

        for selection in self.file_listbox.curselection():
            self.selected_csv_files.append(self.all_csv_files[selection])

        print self.selected_csv_files

    def load_wordlist(self):

        self.word_list_file = tkFileDialog.askopenfilename()

        print self.word_list_file

    def export_csv(self):

        print "hello"


if __name__ == "__main__":
    root = Tk()
    MainWindow(root)
    root.mainloop()