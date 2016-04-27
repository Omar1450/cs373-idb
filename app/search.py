class SearchResult:
    def __init__(self, type, id, obj):
        self.type = type
        self.id = id
        self.obj = obj
        self.context = set()

    def copy(self):
        other = SearchResult(self.type, self.id, self.obj)
        return other

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id

    def __hash__(self):
        return hash((self.type, self.id))
    
    def to_json(self, result_type):
        return {"type": self.type, 
                "name": self.obj.name,
                "url":  self.type + '/' + str(self.id),
                "id": self.id,
                "result_type": result_type,
                "context": list(self.context)}
