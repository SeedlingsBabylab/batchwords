from Tkinter import *
import tkFileDialog
import os
import csv

class MainWindow:

    def __init__(self, master):

        self.csv_directory = None       # the absolute path of the directory chosen
        self.all_csv_files = []         # all file names under the csv_directory
        self.selected_csv_files = []    # integers representing the index of files chosen (from self.all_csv_files)

        self.word_list_file = None
        self.word_list = []

        self.export_file = None

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

        self.both_selected_button = Radiobutton(self.main_frame,
                                                text="both",
                                                variable=self.av_int_var,
                                                value=3)

        self.video_selected_button.grid(row=3, column=3)
        self.audio_selected_button.grid(row=3, column=4)
        self.both_selected_button.grid(row=3, column=5)


        self.file_listbox_label = Label(self.main_frame, text="Files")
        self.file_listbox_label.grid(row=0, column=0)



        self.file_listbox = Listbox(self.main_frame,
                                    width=34,
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
                                             text="Clear All",
                                             command=self.directory_clear)

        self.file_list_clear_button.grid(row=5, column=0)


        self.file_selected_clear_button = Button(self.main_frame,
                                                 text="Clear Selected",
                                                 command=self.clear_selected)

        self.file_selected_clear_button.grid(row=4, column=0)


        self.files_selected_label = Label(self.main_frame, text="files selected", fg="green")


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


        self.clear_wordlist_button = Button(self.main_frame,
                                            text="Clear",
                                            command=self.clear_wordlist)

        self.clear_wordlist_button.grid(row=3, column=1)



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

        self.files_selected_label.grid_remove()

    def select_files(self):

        #TODO make sure you can only select a file once (clear then reselect might re-add)

        print self.file_listbox.curselection()

        for selection in self.file_listbox.curselection():
            self.selected_csv_files.append(self.all_csv_files[selection])

        self.files_selected_label.grid(row=6, column=0)
        print self.selected_csv_files

    def clear_selected(self):

        self.file_listbox.select_clear(0, END)
        self.files_selected_label.grid_remove()

    def load_wordlist(self):

        self.word_list_file = tkFileDialog.askopenfilename()

        with open(self.word_list_file, "rU") as file:
            for line in file:
                self.word_list.append(line.strip())
        print self.word_list_file
        print self.word_list

        for i, word in enumerate(self.word_list):
            self.wordlist_box.insert(i, word)

    def clear_wordlist(self):

        self.word_list_file = None
        self.word_list = []
        self.wordlist_box.delete(0, END)

    def export_csv(self):

        if (not self.word_list) or\
                (not self.word_list_file) or\
                (not self.all_csv_files) or\
                (not self.csv_directory):
            raise Exception("you need to load all the files first")

        results = []
        for file in self.selected_csv_files:
            results.append(self.pull_out_matches(file, self.word_list))

        self.export_file = tkFileDialog.asksaveasfilename()

        with open(self.export_file, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Child_Visit",      # write the header
                            "word",
                            "utterance_type",
                            "object_present",
                            "speaker",
                            "basic_level",
                            "audio_video"])

            print results

            type = self.av_int_var.get()

            for matches in results:

                for entry in matches[1]:

                    if (matches[0][1] is "audio"):  # if the file was an audio csv, pull out
                        if type is 1:               # the data in the appropriate way and write it
                            continue                # to the export csv

                        writer.writerow([matches[0][0],     # child_visit
                                         entry[1],          # word
                                         entry[2],          # utterance_type
                                         entry[3],          # object_present
                                         entry[4],          # speaker
                                         entry[6],          # basic_level
                                         matches[0][1]])    # audio_video

                    else:   # file was video

                        if type is 2:
                            continue
                        writer.writerow([matches[0][0],     # child_visit
                                         entry[3],          # word
                                         entry[4],          # utterance_type
                                         entry[5],          # object_present
                                         entry[6],          # speaker
                                         entry[7],          # basic level
                                         matches[0][1]])    # audio_video

    def pull_out_matches(self, scan_file, wordlist):
        """

        :param scan_file: file to be scanned
        :param word: word to be pulled out
        :return: list of strings representing entries from the scanned file
        """

        matches = []

        file_type = scan_file.find("audio")

        if file_type is -1:
            file_type = "video"
        else:
            file_type = "audio"

        meta_info = (scan_file[0:5], file_type)  #(child_visit, audio/video)

        with open(os.path.join(self.csv_directory, scan_file), "rU") as file:
            reader = csv.reader(file)

            for line in reader:

                if file_type is "audio":
                    if line[6].strip() in wordlist:
                        matches.append(line)
                elif file_type is "video":
                    if line[7].strip() in wordlist:
                        matches.append(line)

        print "meta_info: " + str(meta_info)
        print "matches: " + str(matches)
        return (meta_info, matches)


if __name__ == "__main__":
    root = Tk()
    MainWindow(root)
    root.mainloop()