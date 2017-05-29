class LowerBoundConflict(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.next = None
        self.previous = None

        left.lb_conflict_right = self
        right.lb_conflict_left = self

    def __str__(self):
        return '(' + str(self.left.info.key) + ', ' + str(self.right.info.key) + ')'

    def __repr__(self):
        return '(' + str(self.left.info.key) + ', ' + str(self.right.info.key) + ')'


class UpperBoundConflict(object):
    def __init__(self, node):
        self.node = node
        self.previous = None
        self.next = None

        node.ub_conflict = self

    def __str__(self):
        return '(' + str(self.node.info.key) + ')'

    def __repr__(self):
        return '(' + str(self.node.info.key) + ')'

class DeletedPointerBlock(object):
    def __init__(self, node):
        self.node = node
        self.previous = None
        self.next = None

        node.deleted_pointer_block = self

    def __str__(self):
        return '(' + str(self.node.info.key) + ')'

    def __repr__(self):
        return '(' + str(self.node.info.key) + ')'

