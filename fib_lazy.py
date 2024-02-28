# explanations for member functions are provided in requirements.py
from __future__ import annotations
import math

class FibNodeLazy:

    _id_counter = 0

    def __init__(self, val: int):
        self.id = FibNodeLazy._id_counter
        self.val = val
        self.parent = None
        self.children = []
        self.flag = False
        self.degree = 0
        FibNodeLazy._id_counter += 1

    def get_value_in_node(self):
        return self.val

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag

    def __eq__(self, other: FibNodeLazy):
        return self.val == other.val
    
class FibHeapLazy:
    def __init__(self):
        self.roots = []
        self.min = None
        self.n = 0
        self.dirty = False

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNodeLazy:
        new_node = FibNodeLazy(val)
        self.roots.append(new_node)
        self.n += 1
        
        self.consolidate_if_dirty()

        if self.min is None or new_node.val < self.min.val:
            self.min = new_node
        return new_node
        
    def delete_min_lazy(self) -> None:
        if self.min is None:
            return

        for child in self.min.children:
            self.roots.append(child)
            child.parent = None

        self.roots.remove(self.min)

        if not self.roots:
            self.min = None
        else:
            self.min = self.roots[0]
            self.dirty = True

    def find_min_lazy(self) -> FibNodeLazy:
        self.consolidate_if_dirty()

        return self.min

    def consolidate(self):
        aux = [None] * int(math.log(self.n) * 2)

        for root in self.roots[:]:  
            x = root
            d = x.degree
            while aux[d] is not None:
                y = aux[d]
                if x.val > y.val:
                    x, y = y, x
                self.link(y, x)
                aux[d] = None
                d += 1
            aux[d] = x

        self.roots = [node for node in aux if node is not None]

        self.min = min(self.roots, key=lambda x: x.val, default=None)


    def decrease_priority(self, node: FibNodeLazy, new_val: int) -> None:
        if new_val >= node.val:
            raise ValueError("New value must be smaller than the current value.")
        
        node.val = new_val
        parent = node.parent

        self.consolidate_if_dirty()
        
        if parent and node.val < parent.val:
            self.cut(node, parent)
            self.cascading_cut(parent)
        
        if self.min is None or node.val < self.min.val:
            self.min = node

    def consolidate_if_dirty(self) -> None:
        if self.dirty:
            self.consolidate()
            self.dirty = False

    def cut(self, node: FibNodeLazy, parent: FibNodeLazy) -> None:
        parent.children.remove(node)
        node.parent = None
        self.roots.append(node)
        node.flag = False

    def cascading_cut(self, node: FibNodeLazy):
        parent = node.parent
        if parent:
            if not node.flag:
                node.flag = True
            else:
                self.cut(node, parent)
                self.cascading_cut(parent)

  
    def link(self, y: FibNodeLazy, x: FibNodeLazy) -> None:
        self.roots.remove(y)
        x.children.append(y)
        y.parent = x
        x.degree += 1
        y.flag = False  

#     # feel free to define new methods in addition to the above
#     # fill in the definitions of each required member function (above),
#     # and for any additional member functions you define
