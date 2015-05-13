from Tkinter import *

import ttk
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
        self.root.geometry("900x500")
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
        self.both_selected_button.select()  # both by default

        self.video_selected_button.grid(row=3, column=4)
        self.audio_selected_button.grid(row=3, column=5)
        self.both_selected_button.grid(row=3, column=6)


        # All the file listbox variables and GUI elements
        self.file_listbox_label = Label(self.main_frame, text="Files")
        self.file_listbox_label.grid(row=0, column=1)



        self.file_listbox = Listbox(self.main_frame,
                                    width=53,
                                    height=20,
                                    selectmode=MULTIPLE)

        self.file_listbox.grid(row=1, column=1, padx=10)




        self.file_list_load_button = Button(self.main_frame,
                                            text="Load",
                                            command=self.directory_load)

        self.file_list_load_button.grid(row=2, column=1)




        self.file_select_button = Button(self.main_frame,
                                         text="Select",
                                         command=self.select_files)

        self.file_select_button.grid(row=3, column=1)



        self.file_list_clear_button = Button(self.main_frame,
                                             text="Clear All",
                                             command=self.directory_clear)

        self.file_list_clear_button.grid(row=5, column=1)


        self.file_selected_clear_button = Button(self.main_frame,
                                                 text="Clear Selected",
                                                 command=self.clear_selected)

        self.file_selected_clear_button.grid(row=4, column=1)


        self.files_selected_label = Label(self.main_frame, text="files selected", fg="green")


        # All the file extension variables and GUI elements
        self.file_extension = None

        self.file_extension_box = Entry(self.main_frame, width=12)
        self.file_extension_box.grid(row=3, column=0, rowspan=1)

        self.file_extension_label = Label(self.main_frame, text="file extension")
        self.file_extension_label.grid(row=2, column=0, rowspan=1)


        self.filename_contains = None
        self.filename_contains_box = Entry(self.main_frame, width=20)
        self.filename_contains_box.grid(row=5, column=0)

        self.filename_contains_label = Label(self.main_frame, text="filename contains")
        self.filename_contains_label.grid(row=4, column=0)

        # Word list variables and GUI elements
        self.wordlist_label = Label(self.main_frame, text="Word List")
        self.wordlist_label.grid(row=0, column=2)

        self.wordlist_box = Listbox(self.main_frame,
                                    width=22,
                                    height=20)

        self.wordlist_box.grid(row=1, column=2)


        self.load_wordlist_button = Button(self.main_frame,
                                           text="Load Word List",
                                           command=self.load_wordlist)

        self.load_wordlist_button.grid(row=2, column=2)


        self.clear_wordlist_button = Button(self.main_frame,
                                            text="Clear",
                                            command=self.clear_wordlist)

        self.clear_wordlist_button.grid(row=3, column=2)


        # Final export button
        self.export_csv = Button(self.main_frame, text="Export", command=self.export_csv)
        self.export_csv.grid(row=2, column=4, columnspan=2)


        #self.file_tree = ttk.Treeview(self.main_frame)
        #self.file_tree.grid(row=1, column=3, padx=10)

    def directory_load(self):

        self.directory_clear()

        # get the extension and filename substring for searching/filtering
        self.file_extension = self.file_extension_box.get().strip()
        self.filename_contains = self.filename_contains_box.get()

        print "extension: " + str(self.file_extension) + "######"

        self.csv_directory = tkFileDialog.askdirectory()

        all_files = []

        for dir, subdirs, files in os.walk(self.csv_directory):
            print "dir: " + str(dir) + "\nsubdirs: " + str(subdirs) + "\nfiles: " + str(files) + "\n\n"
            print
            for file in files:

                all_files.append(os.path.join(dir, file))
                # if file.endswith(self.file_extension):
                #     if not self.filename_contains_box.get(): # check if filename_contains is empty
                #         self.all_csv_files.append(file)
                #     elif file.find(self.filename_contains) is not -1:
                #         self.all_csv_files.append(file)
                #print os.path.join(subdir, file)
                #print self.all_csv_files
            print "results: " + str(all_files)
            print "common prefix: " + os.path.commonprefix(all_files)

        self.csv_directory = os.path.commonprefix(all_files)
        prefix_len = len(self.csv_directory)

        for i, file in enumerate(all_files):
            print "filename: " + file[prefix_len:]
            if file.endswith(self.file_extension):
                if not self.filename_contains_box.get(): # check if filename_contains is empty
                    self.all_csv_files.append(file[prefix_len:])
                elif file[prefix_len:].find(self.filename_contains) is not -1:
                    self.all_csv_files.append(file[prefix_len:])
            # if file.endswith(self.file_extension):
            #     if not self.filename_contains_box.get():    # if extension is not provided, continue
            #         continue
            # else:
            #     del all_files[i]


        print "results after filtering: " + str(all_files)






        for i, file in enumerate(self.all_csv_files):
            filename = os.path.split(file)[1]
            self.file_listbox.insert(i, filename)

    def directory_clear(self):

        del self.all_csv_files[:]
        del self.selected_csv_files[:]
        if self.file_extension is not None:
            del self.file_extension

        self.file_listbox.delete(0, END)

        self.files_selected_label.grid_remove()

    def select_files(self):

        print self.file_listbox.curselection()

        for selection in self.file_listbox.curselection():
            print self.all_csv_files[int(selection)]
            if self.all_csv_files[int(selection)] not in self.selected_csv_files:
                self.selected_csv_files.append(self.all_csv_files[int(selection)])

        if len(self.selected_csv_files) > 0:
            self.files_selected_label.grid(row=6, column=1)
        print self.selected_csv_files

    def clear_selected(self):

        self.file_listbox.select_clear(0, END)
        self.files_selected_label.grid_remove()
        del self.selected_csv_files[:]

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
                                         matches[0][1],     # audio_video
                                         matches[0][2]])    # rel_filename

                    else:   # file was video

                        if type is 2:
                            continue
                        writer.writerow([matches[0][0],     # child_visit
                                         entry[3],          # word
                                         entry[4],          # utterance_type
                                         entry[5],          # object_present
                                         entry[6],          # speaker
                                         entry[7],          # basic level
                                         matches[0][1],     # audio_video
                                         matches[0][2]])    # filename


    def pull_out_matches(self, file, wordlist):
        """

        :param scan_file: file to be scanned (relative path from self.csv_directory)
        :param word: word to be pulled out
        :return: list of strings representing entries from the scanned file
        """

        matches = []
        scan_file = os.path.split(file)[1]
        file_type = scan_file.find("audio")

        if file_type is -1:
            file_type = "video"
        else:
            file_type = "audio"

        meta_info = (scan_file[0:5], file_type, scan_file)  #(child_visit, audio/video, rel_filename)

        with open(os.path.join(self.csv_directory, file), "rU") as file:
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