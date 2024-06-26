import tkinter
from typing import List
import math
import custom_platform as pl

_platform: pl.custom_platform = object.__new__(pl.custom_platform)


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    # Search function

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    #  Applying Kruskal algorithm
    def kruskal_algo(self):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
        for u, v, weight in result:
            print("%d - %d: %f" % (u, v, weight))


def load_dataset_from_txt(file_path: str, n: int = 10000):
    """Loads graph from .txt file and returns tuples. Assumes removal of text at the beginning of the
    dataset."""
    dataset = []
    with open(file_path, 'r') as file:
        for line in file:
            from_node, to_node = line.strip().split()
            if int(from_node) > n - 1:
                break
            dataset.append((int(from_node) + 1, int(to_node) + 1))
    return dataset


def matrix_data(dataset: List[tuple], n: int) -> List[List[float]]:
    """Create a nxn matrix and assign weights accordingly"""
    matrix2 = [[0.0 for _ in range(n)] for _ in range(n)]
    for (i, j) in dataset:
        if i > n or j > n:
            continue
        matrix2[i - 1][j - 1] = math.exp(-(i + j) / (min(i, j)))
    return matrix2


def gui_main(user_id):
    global _platform
    content_filtering = False
    recommend_number = 5
    relevancy, ids = _platform.recommender(user_id+1, recommend_number)
    current_reel = 0

    def config():
        vidIdLabel.config(text="Video Id:" + str(ids[current_reel]))
        vidTagsLabel.config(text="Tags:" + " ".join(['#' + tag for tag in
                                                     _platform.reels[current_reel].tags]))

    def refresh():
        nonlocal current_reel, relevancy, ids
        current_reel = 0
        relevancy, ids = _platform.recommender(user_id+1, recommend_number, 1)
        config()

    def change_id(value):
        nonlocal current_reel
        if value < 0:
            return
        if value >= recommend_number:
            refresh()
            return
        print("Reel id:" + str(ids[current_reel]))
        _platform.users[user_id].watch_video(_platform.reels[ids[current_reel]-1])
        current_reel = value
        config()

    # Main Tkinter Window
    mainWindow = tkinter.Tk()
    # Title
    mainWindow.title(_platform.name)
    mainWindow.geometry("360x640")
    # Video ID label:
    vidIdLabel = tkinter.Label(mainWindow, text="Video Id:" + str(ids[current_reel]))
    vidIdLabel.pack()
    # Video Tags label:
    vidTagsLabel = tkinter.Label(mainWindow, text="Tags:" + " ".join(['#' + tag for tag in
                                                                      _platform.reels[current_reel].tags]))
    vidTagsLabel.pack()
    # Scroll Up Button (Go back to previous video)
    upButton = tkinter.Button(mainWindow, text="Scroll Up", command=lambda: change_id(current_reel - 1))
    upButton.pack()
    # Image Rectangle
    # Frame
    vidFrame = tkinter.Frame(mainWindow, width=270, height=480)
    vidFrame.pack()
    # Canvas
    vidCanvas = tkinter.Canvas(vidFrame, width=270, height=480)
    vidCanvas.pack()
    # Like and Dislike buttons
    likeButton = tkinter.Button(vidFrame, text="Like",
                                command=lambda: _platform.users[user_id].like_video(_platform.reels[
                                                                                        ids[current_reel]-1]))
    dislikeButton = tkinter.Button(vidFrame, text="Dislike",
                                   command=lambda: _platform.users[user_id].dislike_video(_platform.reels[
                                                                                              ids[current_reel]-1]))
    likeButton.pack(side=tkinter.LEFT)
    dislikeButton.pack(side=tkinter.RIGHT)
    vidCanvas.create_rectangle(0, 0, 270, 480, fill='lightgrey')
    # Scroll Down Button (Go to next video)
    downButton = tkinter.Button(mainWindow, text="Scroll Down", command=lambda: change_id(current_reel + 1))
    downButton.pack()
    # Main Loop
    mainWindow.mainloop()


def create_platform():
    global _platform
    name = input("Enter name of platform: ")
    tag_count = max(0, int(input("Enter number of tags(0 for default tags): ")))
    tags = None
    if tag_count != 0:
        tags = []
        for i in range(tag_count):
            tag = input(f"Enter tag {i + 1}: ")
            tags.append(tag)
    platform_ = pl.custom_platform(name, tags)
    print("Platform has been created!")
    print(platform_)
    choice = 0
    while True:
        choice = int(input("\n1.Edit name\n2.Edit tags\n3.Generate platform\n4.Save platform \n5"
                           ".Return to main\nEnter choice: "))
        if choice == 1:
            name = input("Enter name of platform: ")
            platform_.name = name
            print("Platform name has been edited!")
            print(platform_)
        elif choice == 2:
            tag_count = max(0, int(input("Enter number of tags(0 for default tags): ")))
            tags = None
            if tag_count != 0:
                tags = []
                for i in range(tag_count):
                    tag = input(f"Enter tag {i + 1}: ")
                    tags.append(tag)
            platform_.tags = tags
            print("Platform tags have been edited")
            print(platform_)
        elif choice == 3:
            default_generation = input("Do you want default generation?(Y/N): ").lower()
            if default_generation != 'y':
                user_count = max(1, int(input("Enter number of initial users: ")))
                reel_count = max(1, int(input("Enter number of reels: ")))
                norm_mean = max(1, int(input("Enter average number of reels watched per user already: ")))
                tag_count = max(1, int(input("Enter average number of tags associated with each video: ")))
                friend_count = max(0, int(input("Enter average number of friends per user already: ")))
                platform_.generate_platform(user_count, reel_count, norm_mean, tag_count=tag_count,
                                            friend_count=friend_count)
            else:
                platform_.generate_platform()
            print("Platform has been generated!")
            print(platform_.users)
            print(platform_.reels)
        elif choice == 4:
            # TODO Save Platform
            _platform = platform_
        elif choice == 5:
            return platform_
        else:
            print("Invalid Choice!")


# TODO load from saved platform
def load_platform():
    global _platform
    platform_: pl.custom_platform = _platform
    username = ''
    password = ''
    logged_in = False
    user_id = None
    while not logged_in:
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        for user in platform_.users:
            if user.username == username and user.password == password:
                logged_in = True
                user_id = user.ID
                print("Logged in!")
                break
        if not logged_in:
            print("Wrong username or password!")
    if logged_in:
        gui_main(user_id-1)


def main():
    global _platform
    # gui_main()
    '''
    n = 10
    txt_file_path = "src/data/Data.txt"
    g = Graph(n)
    dataset = load_dataset_from_txt(txt_file_path, n)
    matrix = matrix_data(dataset, n, g)
    print(matrix)
    print(f"For {n} nodes:\nMinimum Spanning Tree:")
    g.kruskal_algo()
    '''
    choice = 0
    while True:
        choice = int(input("Reel Recommendation System:\n1.Create Platform\n2.Load Platform\n3.Exit\nEnter Choice: "))
        if choice == 1:
            _platform = create_platform()
        elif choice == 2:
            load_platform()
        elif choice == 3:
            print("Exiting!")
            break
        else:
            print("Invalid choice!")
            continue
    '''
    instagram = pl.custom_platform("Instagram")
    instagram.generate_platform(reel_count=50000)
    print(instagram)
    #print(instagram.users)
    #print(instagram.reels)
    x = instagram.recommender(1, 10)
    print(type(x))
    instagram.recommender(2, 10)
    print("Exiting!")
    '''


if __name__ == '__main__':
    main()
