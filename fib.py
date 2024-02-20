# explanations for member functions are provided in requirements.py
from __future__ import annotations

class FibNode:
    def __init__(self, val: int):
        self.val = val
        self.parent = None
        self.children = []
        self.flag = False
        self.degree = 0

    def get_value_in_node(self):
        return self.val

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag

    def __eq__(self, other: FibNode):
        return self.val == other.val

class FibHeap:
    def __init__(self):
        # you may define any additional member variables you need
        self.roots = []
        self.min = None
        pass

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNode:
        new_node = FibNode(val)
        self.roots.append(new_node)

        # Update the minimum node if necessary
        if self.min is None or new_node.val < self.min.val:
            self.min = new_node
        
        return new_node
        
    def delete_min(self) -> None:
            if self.min is None:
                return

            # Add children of the min node to the roots list and clear their parent reference
            for child in self.min.children:
                self.roots.append(child)
                child.parent = None

            # Remove the min node from the roots list
            self.roots.remove(self.min)

            if not self.roots:
                self.min = None
            else:
                self.min = self.roots[0]
                self.consolidate()

    def consolidate(self):
        # Auxiliary array to keep track of degrees
        aux = [None] * len(self.roots)

        for root in self.roots[:]:  # Iterate over a copy since the roots list will be modified
            x = root
            d = x.degree
            while aux[d] is not None:
                y = aux[d]
                if x.val > y.val:
                    x, y = y, x  # Ensure that x has the smaller value
                self.link(y, x)
                aux[d] = None
                d += 1
            aux[d] = x

        # Rebuild the roots list and find the new minimum
        self.roots = []
        self.min = None
        for node in aux:
            if node is not None:
                self.roots.append(node)
                if self.min is None or node.val < self.min.val:
                    self.min = node

    def link(self, y: FibNode, x: FibNode) -> None:
        # Remove y from the roots list and make it a child of x
        self.roots.remove(y)
        x.children.append(y)
        y.parent = x
        x.degree += 1

    def find_min(self) -> FibNode:
        return self.min

    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        if new_val >= node.val:
            raise ValueError("New value must be smaller than the current value.")
        
        node.val = new_val
        parent = node.parent

        if parent and node.val < parent.val:
            self.cut(node, parent)
            self.cascading_cut(parent)

        if node.val < self.min.val:
            self.min = node

    def cut(self, node: FibNode, parent: FibNode) -> None:
        parent.children.remove(node)
        parent.degree -= 1
        node.parent = None
        self.roots.append(node)
        node.flag = False

    def cascading_cut(self, node: FibNode):
        parent = node.parent
        if parent:
            if not node.flag:
                node.flag = True
            else:
                self.cut(node, parent)
                self.cascading_cut(parent)


    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define
