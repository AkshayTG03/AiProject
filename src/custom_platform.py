import random


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

        def __repr__(self):
            return f"ID:{self.ID} Tags: {self.tags} Length: {self.length} \n"

    class User:
        def __init__(self, ID, username=None, password=None, liked=None, disliked=None, watch_history=None,
                     friends=None):
            self.friends = friends if friends is not None else []
            self.disliked = disliked if disliked is not None else []
            self.liked = liked if liked is not None else []
            self.watch_history = watch_history if watch_history is not None else []
            self.username = username if username is not None else str(ID)
            self.password = password if password is not None else str(ID)
            self.ID = ID

        def watch_video(self, ID):
            self.watch_history.append(ID)

        def like_video(self, ID):
            self.liked.append(ID)

        def dislike_video(self, ID):
            self.disliked.append(ID)

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
        self.reels = []
        self.users = []

    def __str__(self):
        return ''.join(str(reel) for reel in self.reels)

    def create_user(self, ID):
        # TODO Get info from console and create user
        u = self.User(ID)
        self.users.append(u)

    def create_reel(self, Name, ID, Tags):
        # TODO Get info form console and create reel
        r = self.Reel(Name, ID, Tags)
        self.reels.append(r)

    def generate_platform(self, user_count: int = 50, reel_count: int = 200, peruser: int = 10, devcount: int = 40,
                          tagcount: int = 3, friend_count: int = 10):
        mean = peruser
        standard_deviation = 3
        user_normal_integers = generate_normal_integers(mean, standard_deviation, devcount)
        user_normal_integers = [max(1, i) for i in user_normal_integers]
        friend_normal_integers = generate_normal_integers(friend_count, 3, devcount)
        friend_normal_integers = [max(1, i) for i in friend_normal_integers]
        tag_normal_integers = generate_normal_integers(tagcount, 1, 10)
        tag_normal_integers = [max(1, i) for i in tag_normal_integers]
        length_normal_integers = generate_normal_integers(30, 5, 40)
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
