import tkinter

import math
import random
import custom_platform as pl


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
    """Create a nxn matrix and assign weights accordingly"""
    matrix = [[0] * n for _ in range(n)]
    matrix[1][2] = None
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


def load_platform():
    pass


def create_platform():
    name = input("Enter name of platform: ")
    user_count = max(0, int(input("Enter number of initial users: ")))
    tag_count = max(0, int(input("Enter number of tags(0 for default tags): ")))
    tags = None
    if tag_count != 0:
        tags = []
        for i in range(tag_count):
            tag = input(f"Enter tag {i+1}: ")
            tags.append(tag)
    platform_ = pl.custom_platform(name, tags)



def main():
    # gui_main()
    '''
    n = 10
    txt_file_path = "src/data/Data.txt"
    g = Graph(n)
    dataset = load_dataset_from_txt(txt_file_path, n)
    matrix = matrix_data(dataset, n, g)
    print(f"For {n} nodes:\nMinimum Spanning Tree:")
    g.kruskal_algo()
    '''
    choice = 0
    while True:
        choice = int(input("Reel Recommendation System:\n1.Create Platform\n2.Load Platform\n3.Exit"))
        if choice == 1:
            create_platform()
        elif choice == 2:
            load_platform()
        elif choice == 3:
            print("Exiting!")
            break
        else:
            print("Invalid choice!")
            continue
    instagram = pl.custom_platform("Instagram")
    instagram.generate_platform()
    print(instagram)
    print(instagram.reels)


if __name__ == '__main__':
    main()
