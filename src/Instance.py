from typing import Union
import types

classes = {}
class Instance():
    """
    Root class of all parent-child objects
    """
    def __init_subclass__(cls, class_name, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.ClassName = class_name
        classes[class_name] = cls

    def __init__(self, parent=None):
        self.Name = self.__class__.__name__
        self.ClassName = self.Name
        self.Children: list[Instance] = []
        if parent:
            parent._add_child(self)
        self.Parent = parent
    
    def __getattr__(self, name):
        if c := self.find_first_child(name):
            return c
        raise AttributeError(f"Attribute {name} not found in")

    def __setattr__(self, name, value):
        if name == "Parent":
            if value and not isinstance(value, Instance):
                raise TypeError(f"Non-Instance {value} cannot be a parent to {self}")
            if value == self:
                raise ValueError("Attempt to set self as own parent")
            elif value in self.Children:
                raise ValueError(f"Attempt to to set child of {self} as parent of itself")
            if getattr(self, "Parent", False):
                self.Parent.Children.remove(self)
            if value:
                object.__setattr__(self, "Parent", value)
                self.Parent._add_child(self)
        object.__setattr__(self, name, value)

    def __repr__(self):
        return f"<{self.ClassName} {self.Name}>"

    def __str__(self):
        return self.Name
    
    def __getitem__(self, key):
        if c := self.find_first_child(key):
            return c
        raise KeyError(f"{key} is not a child of {self}")

    def _add_child(self, child):
        self.Children.append(child)

    def find_first_child(self, name, resolve:bool=False) -> Union[object, bool]:
        for child in sorted(self.Children):
            if child.Name == name:
                return child
        return resolve
    
    def get_children(self) -> list[object]:
        return self.Children
    
    def get_descendants(self) -> list[object]:
        descendants = [child for child in self.Children]
        for child in self.Children:
            descendants += child.get_descendants()
        return descendants
    
    def get_ancestors(self) -> list[object]:
        parent = self.Parent
        ancestors = []
        while parent:
            ancestors.append(parent)
            parent = parent.Parent
        return ancestors
    
    def get_full_name(self) -> str:
        return "".join(ancestor.Name + "." for ancestor in reversed(self.get_ancestors())) + self.Name
    
    @staticmethod
    def new(className, parent=None):
        return classes[className](parent)

class Test(Instance, class_name="Test"):
    pass


if __name__ == "__main__":
    Root = Instance()
    Root.Name = "ROOT"
    test = Instance.new("Test")
    test2 = Instance()
    test2.Parent = test
    test.Parent = Root
    print(Root.__repr__())
    print(test.get_children())
    print(test2.get_ancestors())
    print(test2.get_full_name())
    print(Root.get_descendants())
    print(Root.get_full_name())