class SearchResult:
    def __init__(self, type, id, obj):
        self.type = type
        self.id = id
        self.obj = obj

    def fleshOut(self, blah):
        pass

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id

    def __hash__(self):
        return hash((self.type, self.id))
    
    def to_json(self):
        return {"type": self.type, "id": self.id}
