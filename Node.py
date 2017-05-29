class NodeInfo(object):
    def __init__(self, key, height):
        self.key = key
        self.height = height
        self.is_deleted = False


class Node(object):
    def __init__(self, info, skip_list, right=None, left=None, down=None):
        self.info = info
        self.skip_list = skip_list

        self.r = right
        self.l = left
        self.up = None
        self.down = down

        self.ub_conflict = None
        self.lb_conflict_left = None
        self.lb_conflict_right = None
        self.deleted_pointer_block = None

        self.possible_conflict = False
        self.longest_search_path = 0

        self.k = 0
        self.s = 0

    def __str__(self):
        return str(self.key())

    def __repr__(self):
        return str(self.key())

    def right(self):
        node = self.r
        while node is not None and node.info.is_deleted and node.is_not_tail():
            node = node.r
        return node

    def left(self):
        node = self.l
        while node is not None and node.info.is_deleted and node.is_not_head():
            node = node.l
        return node

    def top(self):
        node = self
        while node.up is not None:
            node = node.up
        return node

    def bottom(self):
        node = self
        while node.down is not self.skip_list.bottom:
            node = node.down
        return node

    def key(self):
        return self.info.key

    def is_deleted(self):
        return self.info.is_deleted

    def delete(self):
        self.info.is_deleted = True

    def height(self):
        return self.info.height

    def incr_height(self):
        self.info.height += 1

    def increment_height(self, left, right):
        self.info.height += 1
        new_node = Node(self.info, self.skip_list, right, left, self)
        self.up = new_node
        return new_node

    def decr_height(self):
        self.info.height -= 1

    def is_not_head(self):
        return self.info is not self.skip_list.head.info

    def is_tail(self):
        return self.info is self.skip_list.tail.info

    def is_not_tail(self):
        return self.info is not self.skip_list.tail.info

    def is_bottom(self):
        return self is self.skip_list.bottom

    def has_no_conflict(self):
        return self.ub_conflict is None and self.lb_conflict_left is None and self.lb_conflict_right is None and self.info.is_deleted == False

    def mark_possible_conflict(self):
        x = self.top()
        while x.down is not None:
            x.possible_conflict = True
            x = x.down

    def update_decoration(self):
        if self.r.up is None:
            self.k = self.r.k + self.down.k
            self.s = self.r.s + self.r.k + self.down.s + self.down.k
        else:
            self.k = self.down.k
            self.s = self.down.s + self.down.k

        if (self.height() == 1 or self.up is None) and not self.is_deleted():
            self.k += 1

    def update_longest_search_path(self):
        down = self.down
        right = self.r
        nodes_down = not(down.is_bottom() or (down.is_deleted() and down.longest_search_path == 0))
        nodes_right = not(right.up is not None or (right.is_deleted() and right.longest_search_path == 0) or right.is_tail())
        if nodes_down:
            if nodes_right:
                self.longest_search_path = max(down.longest_search_path, right.longest_search_path) + 1
            else:
                self.longest_search_path = down.longest_search_path + 1
        else:
            if nodes_right:
                self.longest_search_path = right.longest_search_path + 1
            else:
                self.longest_search_path = 0