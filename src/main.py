import tkinter


class Reel:
    def __init__(self, Name, ID, Tags):
        self.name = Name
        self.ID = ID
        self.tags = Tags

    def firstTimeSetup(self):
        pass


class User:
    def __init__(self, ID):
        self.ID = ID
        self.liked = []
        self.disliked = []
        self.watchHistory = []
        self.tags = []

    def watchVideo(self, ID):
        self.watchHistory.append(ID)

    def likeVideo(self, ID):
        self.liked.append(ID)

    def dislikeVideo(self, ID):
        self.disliked.append(ID)


class platform:
    def __init__(self):
        self.tags = ["Food", "Meme", "Travel", "Sports", "Music", "Politics", "Movies"]  # Just for placeholder
        self.reels = []
        self.users = []

    def createUser(self, ID):
        u = User(ID)
        self.users.append(u)

    def createReel(self, Name, ID, Tags):
        r = Reel(Name, ID, Tags)
        self.reels.append(r)


def gui():
    # Main Tkinter Window
    mainWindow = tkinter.Tk()
    #Title
    mainWindow.title("Platform")
    # Main Loop
    mainWindow.mainloop()


def main():
    gui()
    pass


if __name__ == '__main__':
    main()
