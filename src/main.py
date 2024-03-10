import tkinter
import networkx as nx
import matplotlib.pyplot as plt
import os
import scipy
import math


class Reel:
    def __init__(self, Name, ID, Tags):
        self.name = Name
        self.ID = ID
        self.tags = Tags

    def first_time_setup(self):
        pass


class User:
    def __init__(self, ID, userName, password, liked, disliked, watchHistory, tags):
        self.ID = ID
        self.userName = ''
        self.password = ''
        self.liked = []
        self.disliked = []
        self.watch_history = []
        self.tags = []

    def watch_video(self, ID):
        self.watch_history.append(ID)

    def like_video(self, ID):
        self.liked.append(ID)

    def dislike_video(self, ID):
        self.disliked.append(ID)


class platform:
    def __init__(self):
        self.tags = ["Food", "Meme", "Travel", "Sports", "Music", "Politics", "Movies"]  # Just for placeholder
        self.reels = []
        self.users = []

    def create_user(self, ID):
        u = User(ID)
        self.users.append(u)

    def create_reel(self, Name, ID, Tags):
        r = Reel(Name, ID, Tags)
        self.reels.append(r)


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


def matrix_data(dataset, n, g):
    """Create a nxn matrix and assign weights according"""
    matrix = [[0] * n for _ in range(n)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if (i, j) in dataset:
                matrix[i - 1][j - 1] = math.exp(-(i + j) / (min(i, j)))
                g.add_edge(i - 1, j - 1, matrix[i - 1][j - 1])
    return matrix


def gui_main():
    # Main Tkinter Window
    mainWindow = tkinter.Tk()
    # Title
    mainWindow.title("Platform")
    mainWindow.geometry("360x640")
    # Video ID label:
    vidIdLabel = tkinter.Label(mainWindow, text="Video Id:")
    vidIdLabel.pack()
    # Video Tags label:
    vidTagsLabel = tkinter.Label(mainWindow, text="Tags:#food #meme")
    vidTagsLabel.pack()
    # Scroll Up Button (Go back to previous video)
    upButton = tkinter.Button(mainWindow, text="Scroll Up")
    upButton.pack()
    # Image Rectangle
    # Frame
    vidFrame = tkinter.Frame(mainWindow, width=270, height=480)
    vidFrame.pack()
    # Canvas
    vidCanvas = tkinter.Canvas(vidFrame, width=270, height=480)
    vidCanvas.pack()
    # Like and Dislike buttons
    likeButton = tkinter.Button(vidFrame, text="Like")
    dislikeButton = tkinter.Button(vidFrame, text="Dislike")
    likeButton.pack(side=tkinter.LEFT)
    dislikeButton.pack(side=tkinter.RIGHT)
    vidCanvas.create_rectangle(0, 0, 270, 480, fill='lightgrey')
    # Scroll Down Button (Go to next video)
    downButton = tkinter.Button(mainWindow, text="Scroll Down")
    downButton.pack()
    # Main Loop
    mainWindow.mainloop()


def main():
    # gui_main()
    n = 100
    txt_file_path = "src/data/Data.txt"
    g = Graph(n)
    dataset = load_dataset_from_txt(txt_file_path, n)
    matrix = matrix_data(dataset, n, g)
    g.kruskal_algo()


if __name__ == '__main__':
    main()
