
"""
class Inventory():
    def __init__(self):
        self.dict = {}
        self.current = None
        self.listOfAllObjects = []
        
    def select(self, name):
        self.current = self.dict[name]
    
    def add(self, object):
        self.dict[object.name] = object
        self.listOfAllObjects.append(object.name)
        
    def remove(self, name):
        self.dict.remove(name)
        self.current = None;
    
    def hasEverHad(self, name):
        if self.listOfAllObjects.count(name) > 0:
            return True;
        else:
            return False;
       
 """    
