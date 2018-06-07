class MemoryCollection:
    def __init__(self, id, baby_id, created_at, months, days, layout, caption, obj):
        self.id = id
        self.baby_id = baby_id
        self.created_at = created_at
        self.months = months
        self.days = days
        self.layout = layout
        self.layout_id_list = []
        self.caption = caption
        # self.memory = Memory(obj)

    def store(self):
        pass


class Memory:
    def __init__(self, id, content, photo_path, video_path):
        self.id = id
        self.content = content
        self.src_url = video_path if video_path else photo_path

    def store(self):
        pass

memoryCollectionSet = set()
memorySet = set()

def printabc():
    print('---------------')
