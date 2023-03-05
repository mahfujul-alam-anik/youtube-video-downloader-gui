import customtkinter as ctk
from pytube import YouTube

# system settings
ctk.set_appearance_mode('dark')
# ctk.set_default_color_theme('blue')


# define an app 
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # set frame size
        self.geometry('720x480')
        self.title('YouTube Video Downloader (by Anik)')

        # make some padding in top 
        ctk.CTkLabel(self, text="").pack(pady=30)

        # make input box for taking url
        self.boxLabel = ctk.CTkLabel(self, text="Input your Youtube video URL", font=('Arial Black', 20))
        self.boxLabel.pack(pady=30)
        self.inputBox = ctk.CTkEntry(self, width=400, height=40)
        self.inputBox.pack()

        # make button and call the download function 
        self.button = ctk.CTkButton(self, text="Start Download", font=('Arial Black', 13), command=self.startDownload)
        self.button.pack(pady=15)

        # define an finish label to understand video downloaded or not
        self.finish_label = ctk.CTkLabel(self, text="")
        self.finish_label.pack(pady=5) 

        # define progress percentage and progress bar 
        self.p_percentage = ctk.CTkLabel(self, text="", text_color="blue")
        self.p_percentage.pack(padx=10)
        self.progress_bar = ctk.CTkProgressBar(self, width=500, height=20)
        self.progress_bar.set(0)
        self.progress_bar.pack_forget()
        

    # video download function 
    def startDownload(self):
        try:
            self.finish_label.configure(text="") # make alert box empty
            self.boxLabel.configure(text="Input your Youtube video URL") # make label box empty
            self.progress_bar.pack_forget() # reset the progress bar
            self.p_percentage.configure(text="") # reset percentage label

            # start process to download video 
            video_url = self.inputBox.get()
            ytObj = YouTube(video_url, on_progress_callback=self.countProgress)
            stream_ = ytObj.streams.get_highest_resolution()
            stream_.download(output_path='Videos') # download video in Videos folder

            # alert after download and show the video title
            self.finish_label.configure(text="Download Complete!", text_color='green')
            self.boxLabel.configure(text=f"Video Title: {stream_.title}", font=('Arial Black', 14))
        except:
            # error alert
            self.finish_label.configure(text="Download Error!", text_color="red")


    #progress count and update
    def countProgress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        bytes_downloaded_percent = bytes_downloaded / total_size * 100
        percentage = str(int(bytes_downloaded_percent))

        # update progress & progress bar
        self.p_percentage.configure(text=f"{percentage}%")
        self.p_percentage.update()
        self.progress_bar.set(float(percentage) / 100)
        if self.progress_bar.get() > 0:
            self.progress_bar.pack(padx=10)
        self.progress_bar.update()


# initialization & run the app 
app = App()
app.mainloop()
