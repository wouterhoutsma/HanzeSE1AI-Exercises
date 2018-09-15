nodes = []


class Node:
    def __init__(self, left, right, parent=None):
        self.left = left
        self.right = right
        self.children = []
        self.parent = parent

    def generate_children(self):
        if 'F' in self.left:
            left_copy = set(self.left)
            right_copy = set(self.right)
            left_copy.remove('F')
            right_copy.add('F')
            # Make a node with only a moved farmer
            new_node = Node(left_copy.copy(), right_copy.copy(), self)
            self.children.append(new_node)
            # Move farmer and another character to the right
            for element in left_copy:
                left_copy.remove(element)
                right_copy.add(element)
                new_node = Node(left_copy.copy(), right_copy.copy(), self)
                self.children.append(new_node)
                right_copy.remove(element)
                left_copy.add(element)
        else:
            if len(self.left) == 0:
                return
            left_copy = set(self.left)
            right_copy = set(self.right)
            right_copy.remove('F')
            left_copy.add('F')
            # Make a node with only a moved farmer
            new_node = Node(left_copy.copy(), right_copy.copy(), self)
            self.children.append(new_node)
            # Move farmer and another character to the left
            for element in right_copy:
                # Remove element from right copy, add to left copy: this is our move
                right_copy.remove(element)
                left_copy.add(element)

                new_node = Node(left_copy.copy(), right_copy.copy(), self)
                self.children.append(new_node)

                # Re-add the element to  the right copy, and remove from left copy.
                left_copy.remove(element)
                right_copy.add(element)

    def state(self):
        return ''.join(self.left) + '|' + ''.join(self.right)

    def is_valid(self):
        sides = [self.left, self.right]
        for side in sides:
            if 'F' in side:
                continue
            if 'G' in side and 'C' in side:
                return False
            if 'G' in side and 'W' in side:
                return False
        return True

    def is_goal(self):
        return len(self.left) == 0


left = {'F', 'G', 'C', 'W'}
right = set()
node = Node(left, right)
nodes.append(node)
node.generate_children()


# Alternative to overriding the hash function of the node object
# This is important because the memory signature of sets is random
def node_number(comparison_node):
    number = 0
    number = number + 1 if 'C' in comparison_node.left else number + 10
    number = number + 100 if 'G' in comparison_node.left else number + 1000
    number = number + 10000 if 'W' in comparison_node.left else number + 100000
    number = number + 1000000 if 'F' in comparison_node.left else number + 10000000
    return number


def dfs(node_list):
    global nodes
    for node in node_list:
        if node_number(node) not in nodes:
            nodes.append(node_number(node))
            if node.is_valid():
                if node.is_goal():
                    return node
                node.generate_children()
                return dfs(node.children)
            else:
                continue


answer = dfs(node.children)
parents = list()
parents.append(answer)
while answer.parent is not None:
    parents.append(answer.parent)
    answer = answer.parent
parents.reverse()
for el in parents:
    print(el.state())
