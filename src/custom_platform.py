import random
import sys
import time
from typing import List, Union


def generate_normal_integers(mean, std_dev, count):
    integers = []
    for _ in range(count):
        integer = round(random.gauss(mean, std_dev))
        integers.append(integer)
    integers.sort()
    return integers


class custom_platform:
    class Reel:
        def __init__(self, id_, tags, length: int):
            self.ID = id_
            self.tags = tags
            self.length = length
            self.likes = 0
            self.dislikes = 0

        def __repr__(self):
            return f"ID:{self.ID} Tags: {self.tags} Length: {self.length} \n"

    class User:
        def __init__(self, ID, username=None, password=None, liked=None, disliked=None, watch_history=None,
                     friends=None):
            self.friends = friends if friends is not None else []
            self.disliked = disliked if disliked is not None else []
            self.liked = liked if liked is not None else []
            self.watch_history = watch_history if watch_history is not None else []
            self.username = str(username) if username is not None else str(ID)
            self.password = str(password) if password is not None else str(ID)
            self.ID = ID

        def __repr__(self):
            return (f"User:{self.ID} Friends: {self.friends} \n    Watch History:{self.watch_history}\n    "
                    f"Liked: {self.liked}\n")

        def watch_video(self, reel: 'custom_platform.Reel'):
            if reel not in self.watch_history:
                self.watch_history.append(reel)

        def like_video(self, reel: 'custom_platform.Reel'):
            self.liked.append(reel)
            self.watch_video(reel)
            reel.likes += 1
            print(self)

        def dislike_video(self, reel: 'custom_platform.Reel'):
            self.disliked.append(reel)
            self.watch_video(reel)
            reel.dislikes += 1
            print(self)

        def add_friend(self, ID):
            self.friends.append(ID)

        def remove_friend(self, ID):
            self.friends.remove(ID)

    def __init__(self, name: str, tags=None):
        if tags is None:
            self.tags = ["Food", "Meme", "Travel", "Sports", "Music", "Politics", "Movies"]  # Just for placeholder
        else:
            self.tags = tags
        self.name = name
        self.reels: List[custom_platform.Reel] = []
        self.users: List[custom_platform.User] = []
        self.matrix: List[List[float]] = []

    def __str__(self):
        # return ''.join(str(reel) for reel in self.reels)
        return f"Platform:\nName:{self.name}\nTags:{self.tags}\n"

    def create_user(self, ID):
        # TODO Get info from console and create user
        u = self.User(ID)
        self.users.append(u)

    def create_reel(self, Name, ID, Tags):
        # TODO Get info form console and create reel
        r = self.Reel(Name, ID, Tags)
        self.reels.append(r)

    def create_user_matrix(self):
        user_tag_matrix = [[0.0 for _ in range(len(self.tags))] for _ in range(len(self.users))]
        for i, user in enumerate(self.users):
            for reel in user.watch_history:
                for j, tag in enumerate(self.tags):
                    for vid_tag in reel.tags:
                        if tag == vid_tag:
                            if reel in user.liked:
                                # Liked
                                user_tag_matrix[i][j] += 1
                                break
                            elif reel in user.disliked:
                                # Disliked
                                user_tag_matrix[i][j] -= 1
                                break
                            else:
                                # Just Viewed
                                user_tag_matrix[i][j] += 0.25
                                break
        return user_tag_matrix

    def create_reel_matrix(self):
        reel_matrix = [[0 for _ in range(len(self.tags))] for _ in range(len(self.reels))]
        for i, reel in enumerate(self.reels):
            for j, tag in enumerate(self.tags):
                for reel_tag in reel.tags:
                    if tag == reel_tag:
                        reel_matrix[i][j] += 1
        return reel_matrix

    def matrix_factorization(self):
        print("Beginning User Factorization!")
        start_time = time.time()
        user_matrix = self.create_user_matrix()
        print(f"Finished User Factorization in {(time.time() - start_time) * 1000:.2f} milliseconds")
        # print("User Matrix:\n" + str(user_matrix))
        print("Beginning Reel Factorization!")
        start_time = time.time()
        reel_matrix = self.create_reel_matrix()
        print(f"Finished Reel Factorization in {(time.time() - start_time) * 1000:.2f} milliseconds")
        # print("Reel Matrix:\n" + str(reel_matrix))
        print("Beginning Matrix Factorization!")
        start_time = time.time()
        user_length = len(self.users)
        reel_length = len(self.reels)
        resultant_matrix = [[0.0 for _ in range(len(self.reels))] for _ in range(len(self.users))]
        for i in range(len(self.users)):
            progress = round(((i + 1) / user_length) * 100, 2)
            time_per_progress = (time.time() - start_time) / progress
            eta = (100 - progress) * time_per_progress
            sys.stdout.write(f'\rProgress: {progress}% ETA:{eta:.0f}s')
            sys.stdout.flush()
            for j in range(len(self.reels)):
                for k in range(len(self.tags)):
                    resultant_matrix[i][j] += user_matrix[i][k] * reel_matrix[j][k]
        print(f"\nFinished Matrix Factorization in {(time.time() - start_time) * 1000:.2f} milliseconds")
        return resultant_matrix

    def recommender(self, id_: int, n: int, refresh=0):
        if refresh == 1:
            self.matrix = self.matrix_factorization()
        matrix = self.matrix
        u: Union[custom_platform.User, None] = None
        for user in self.users:
            if user.ID == id_:
                u = user
        user_row = matrix[id_ - 1]
        view_history = u.watch_history
        unseen_row = [user_row[i] for i in range(len(user_row)) if i not in view_history]
        vid_ids = [i for i in range(len(user_row)) if i not in view_history]
        unseen_row, vid_ids = zip(*sorted(zip(unseen_row, vid_ids), key=lambda x: x[0], reverse=True))
        print(f"Here are the recommended videos and their relevancy for user {id_}:")
        print(' '.join([f'[{vid}:{row}]' for row, vid in zip(unseen_row[:n], vid_ids[:n])]))
        return unseen_row[:n], vid_ids[:n]

    '''
    def check_relevancy(self, reel1, reel2):
        for i in reel2.tags:
            for j in reel2.tags:
                if i == j:
                    match +=1
        return match/max(len(reel1.tags), len(reel2.tags))
    def start(self):
        for i in self.reels:
            for j in self.reels[i:]:
                weight = check_relevancy()
                g.add_edge(i.ID,j.ID, weight)
    '''
    def generate_platform(self, user_count: int = 200, reel_count: int = 5000, per_user: int = 10, dev_count: int = 40,
                          tag_count: int = 3, friend_count: int = 10):
        mean = per_user
        standard_deviation = 3
        user_normal_integers = generate_normal_integers(mean, standard_deviation, dev_count)
        user_normal_integers = [max(1, i) for i in user_normal_integers]
        friend_normal_integers = generate_normal_integers(friend_count, 3, dev_count)
        friend_normal_integers = [max(0, i) for i in friend_normal_integers]
        tag_normal_integers = generate_normal_integers(tag_count, 1, 10)
        tag_normal_integers = [max(1, i) for i in tag_normal_integers]
        length_normal_integers = generate_normal_integers(30, 15, 40)
        length_normal_integers = [max(1, i) for i in length_normal_integers]

        # Generate reels
        for i in range(reel_count):
            # Choose number of tags based on normal distribution
            n = random.sample(tag_normal_integers, 1)
            # Choose n random tags from all tags in platform
            t = random.sample(self.tags, n[0])
            length = random.sample(length_normal_integers, 1)
            r = self.Reel(i + 1, t, length[0])
            self.reels.append(r)

        full_user_ids = [i for i in range(1, user_count + 1)]
        # Generate Users
        for i in range(user_count):
            # Choose number of reels user has already seen based on normal distribution
            n = random.sample(user_normal_integers, 1)
            # Friend Count
            f = random.sample(friend_normal_integers, 1)
            # Choose n random reels
            reels = random.sample(self.reels, n[0])
            # Choose f random friends
            friends = random.sample(full_user_ids, f[0])
            number_likes = random.randint(0, n[0])
            number_dislikes = random.randint(0, n[0] - number_likes)
            liked_reels = random.sample(reels, number_likes)
            remaining_reels = [reel for reel in reels if reel not in liked_reels]
            disliked_reels = random.sample(remaining_reels, number_dislikes)
            u = self.User(i + 1, i + 1, i + 1, liked_reels, disliked_reels, reels, friends)
            self.users.append(u)
        self.matrix = self.matrix_factorization()
