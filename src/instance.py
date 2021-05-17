from typing import Union

classes = {}
class Instance():
    """
    Root class of all parent-child objects
    """
    def __init_subclass__(cls, class_name, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.class_name = class_name
        classes[class_name] = cls

    def __init__(self, parent=None):
        self.name = self.__class__.__name__
        self.class_name = self.name
        self.children: list[Instance] = []
        self.parent = parent

    def __getattr__(self, name):
        if c := self.find_first_child(name):
            return c
        if c := object.__getattribute__(self, name):
            return c
        
        raise AttributeError(f"Attribute {name} not found in {self}")

    def __setattr__(self, name, value):
        if name == "parent":
            if value and not isinstance(value, Instance):
                raise TypeError(f"Non-Instance {value} cannot be a parent to {self}")
            if value == self:
                raise ValueError("Attempt to set self as own parent")
            elif value in self.children:
                raise ValueError(f"Attempt to to set child of {self} as parent of itself")
            if getattr(self, "parent", False):
                self.parent.children.remove(self)
            if value:
                object.__setattr__(self, "parent", value)
                self.parent._add_child(self)
        object.__setattr__(self, name, value)

    def __repr__(self):
        return f"<{self.class_name} {self.name}>"

    def __str__(self):
        return self.name
    
    def __getitem__(self, key):
        if c := self.find_first_child(key):
            return c
        raise KeyError(f"{key} is not a child of {self}")

    def _add_child(self, child):
        self.children.append(child)

    def find_first_child(self, name, resolve:bool=False):
        for child in sorted(self.children, key=lambda c: c.name):
            if child.name == name:
                return child
        return resolve
    
    def get_children(self):
        return self.children
    
    def get_descendants(self):
        descendants = [child for child in self.children]
        for child in self.children:
            descendants += child.get_descendants()
        return descendants
    
    def get_ancestors(self):
        parent = self.parent
        ancestors = []
        while parent:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors
    
    def get_full_name(self) -> str:
        return "".join(ancestor.name + "." for ancestor in reversed(self.get_ancestors())) + self.name
    
    @staticmethod
    def new(class_name, parent=None):
        return classes[class_name](parent)


if __name__ == "__main__":
    Root = Instance()
    Root.name = "ROOT"
    test = Instance()
    test2 = Instance()
    test2.parent = test
    test.parent = Root
    print(Root.__repr__())
    print(test.get_children())
    print(test2.get_ancestors())
    print(test2.get_full_name())
    print(Root.get_descendants())
    print(Root.get_full_name())