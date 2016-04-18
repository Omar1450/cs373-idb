class search_result:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __hash__(self):
        return hash((self.name, self.url))
    
    def to_json(self):
        return {"name": self.name, "url": self.url}
