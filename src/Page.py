from collections.abc import Callable


class Page:
    def __init__(self, name: str, description: str, func: Callable = None) -> None:
        self._name = name
        self._description = description
        self._func = func
        self._items = [] # items[0] is parent page, items[1:] are child page
        
    def getName(self) -> str:
        return self._name
    
    def getDescription(self) -> str:
        return self._description
    
    def getLocation(self) -> str:
        pages = [self._name]
        p = self._items[0]
        while p:
            pages = [p.getName()] + pages
            p = p.listItems()[0]
        return '\\'.join(pages)
    
    def listItems(self) -> list:
        return self._items
    
    def isLeaf(self) -> bool:
        return True if self._func else False
    
    def addItems(self, *items: list):
        if len(items) < 1:
            raise Exception("Items at least have one item: parent item")
        if self._func and len(items) > 1:
            raise Exception("Leaf node should only have one item: parent node")
        self._items += items
        return self
    
    def removeItems(self) -> list:
        self._items = []
        return self
    
    def setParentItem(self, parent):
        if len(self._items) == 0:
            self._items.append(parent)
        else:
            self._items[0] = parent
        return self
        
    def setChildrenItems(self, *children):
        if self._func:
            raise Exception("Leaf node should not have child")
        if len(self._items) == 0:
            self._items.append(None)
        self._items = [self._items[0]] + [*children]
        return self
    
    def _showItems(self):
        for i in range(1, len(self._items)):
            item = self._items[i % len(self._items)]
            print("    {index}. {name:<25s}{description}".format(index=i, name=item.getName(), description=item.getDescription()))
        print("\n    0. Go back\n")

    def next(self):
        if self._func: # 叶子节点
            try:
                self._func()
            except Exception as e:
                print(e)
            input("\nPress enter to exit...")
            return self._items[0]
        else: # 分支节点
            try:
                print("Chose a number below:\n")
                self._showItems()
                user_input = input(self.getLocation() + ' >>> ')
                idx = int(user_input)
                if idx < len(self._items):
                    return self._items[idx]
                return self
            except:
                return self
