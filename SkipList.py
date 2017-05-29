from Node import *
from Conflicts import *
from math import log2, log, ceil
from random import randint
import sys

sys.setrecursionlimit(20000000)

class SkipList(object):
    def __init__(self, ub, rebalance_threshold=-1.0):
        self.bottom = Node(NodeInfo(0, 0), self)
        self.head = Node(NodeInfo(-2147483647, 1), self, None, None, self.bottom)
        self.tail = Node(NodeInfo(2147483647, 1), self, None, self.head, self.bottom)
        self.head.r = self.tail
        self.head.k = 1
        self.size = 0
        self.ub = ub
        self.lb_conflicts = None
        self.next_lb_conflict = None
        self.ub_conflicts = None
        self.next_ub_conflict = None
        self.deleted_pointer_block = None
        self.next_deleted_pointer_block = None
        self.debug = False
        self.decorate = True
        self.rebalance_threshold = rebalance_threshold
        self.rebalance_at_threshold = rebalance_threshold != -1.0

    def height(self):
        return self.head.height()

    # region Updates

    def measure_search_path_length(self, key):
        search_path = [self.head]
        x = self.head
        while True:
            while key >= x.r.key():
                x = x.r
                search_path.append(x)

            if x.down == self.bottom:
                break

            x = x.down
            search_path.append(x)

        if x.height() == 1:
            return len(search_path) - 1
        else:
            return 0

    def measure_search_path_length_all(self, key):
        search_path = [self.head]
        x = self.head
        while True:
            while key >= x.r.key():
                x = x.r
                search_path.append(x)

            if x.down == self.bottom:
                break

            x = x.down
            search_path.append(x)

        while search_path[-1].up is not None:
            search_path.pop()

        return len(search_path) - 1

    def insert(self, key):
        search_path = [self.head]
        x = self.head
        x.possible_conflict = True
        while True:
            while key >= x.r.key():
                x = x.r
                search_path.append(x)
                x.possible_conflict = True

            if x.down == self.bottom:
                break

            x = x.down
            search_path.append(x)
            x.possible_conflict = True
        search_path_length = len(search_path)

        # Insert the node
        node = Node(NodeInfo(key, 1), self, x.r, x, self.bottom)
        node.possible_conflict = True
        x.r.l = node
        x.r = node
        self.size += 1

        # Remove eventual LB conflict
        self.delete_lb_conflict(node.left().lb_conflict_right)
        self.delete_lb_conflict(node.right().lb_conflict_left)

        # Check for upper bound conflict
        self.cuc(node)

        # Decorate
        if self.decorate:
            old_s = self.head.s
            old_k = self.head.k

            if node.r.height() == 1:
                node.k = node.r.k + 1
                node.s = node.r.s + node.r.k
                right_k = node.r.k
            else:
                node.k = 1
                node.s = 0
                right_k = 0
            while len(search_path) > 0:
                search_path.pop().update_decoration()

            try:
                assert (old_k + 1 == self.head.k)
            except AssertionError:
                print('Insert: ' + str(key))
                print('Old k: ' + str(old_k))
                print('New k: ' + str(self.head.k))
                self.print()
                exit()

            try:
                assert (old_s + search_path_length + right_k == self.head.s)
            except AssertionError:
                print('Insert: ' + str(key))
                print('Old s: ' + str(old_s))
                print('right s: ' + str(right_k))
                print('Actual s: ' + str(self.head.s))
                print('Expected s: ' + str(old_s + search_path_length + right_k))
                self.print()
                exit()

        # Threshold rebalancing
        rebalances = 0
        self.update_longest_search_path(node)
        if self.rebalance_at_threshold:
            threshold = ceil(4 * self.height() * self.rebalance_threshold) - 1
            x = node
            moved_left = True
            while x is not None and self.head.longest_search_path > threshold:
                if moved_left:
                    rebalances += self.remove_deleted_nodes_from_sublist(x)
                else:
                    rebalances += self.remove_deleted_nodes_from_sublist(x.r)
                rebalances += self.rebalance_sublist(x)

                if x.up is not None:
                    x = x.up
                    moved_left = False
                else:
                    x = x.left()
                    moved_left = True
            try:
                assert (self.head.longest_search_path <= threshold)
            except AssertionError:
                print('Insert: ' + str(key))
                print('Longest search path: ' + str(self.head.longest_search_path))
                print('Threshold: ' + str(threshold))
                print('size: ' + str(self.size))
                self.print()
                exit()

            try:
                assert (self.head.longest_search_path <= threshold)
            except AssertionError:
                print('Longest search path: ' + str(self.head.longest_search_path))
                print('Threshold: ' + str(threshold))
                print('size: ' + str(self.size))
                self.print()
                exit()

        # Debug
        if self.debug:
            print('Insert: ' + str(key))
            self.print()

        return rebalances

    def delete(self, key):
        node = self.head
        node.possible_conflict = True
        search_path = [node]
        while True:
            while key >= node.r.key():
                node = node.r
                search_path.append(node)
                node.possible_conflict = True

            if node.down == self.bottom:
                break

            node = node.down
            search_path.append(node)
            node.possible_conflict = True

        search_path_length = len(search_path) - node.height()

        # Delete the node
        node.delete()
        self.size -= 1

        x = search_path[-node.height()]
        # Register node for physical deletion
        self.add_deleted_pointer_block(x)

        # Mark deleted node not to be in conflict
        self.delete_ub_conflict(x.ub_conflict)

        # Check for conflicts
        gap_is_empty = False
        if x.left().height() > 1:
            gap_is_empty = self.clc_right(x.left(), x.height())

        if gap_is_empty is False:
            if x.right().height() == x.height():
                self.cuc(x.right())
            else:
                self.cuc(x.left())

        if x.height() > 1:
            self.delete_lb_conflict(x.down.lb_conflict_left)
            self.delete_lb_conflict(x.down.lb_conflict_right)

        h = x.height()
        while x.down is not self.bottom:
            xl = x.left()
            xld = xl.down
            xldr = xld.right()
            x = x.down
            h -= 1
            self.delete_ub_conflict(x.ub_conflict)
            self.delete_lb_conflict(x.lb_conflict_left)
            self.delete_lb_conflict(x.lb_conflict_right)
            if xldr.height() == h:
                self.cuc(xldr, True)
            else:
                self.clc_left(xldr, h)

        # Decoration
        if self.decorate:
            search_path2 = search_path.copy()
            old_s = self.head.s
            old_k = self.head.k
            while len(search_path) > 0:
                search_path.pop().update_decoration()

            try:
                assert (self.head.k == old_k - 1)
            except AssertionError:
                print('Delete: ' + str(node.key()))
                print(node.key() == key)
                print(node.is_deleted())
                print('Old k: ' + str(old_k))
                print('New k: ' + str(self.head.k))
                print( )
                self.print()
                exit()

            try:
                assert (self.head.s == old_s - search_path_length)
            except AssertionError:
                print('Delete: ' + str(node.key()))
                print(node.key() == key)
                print(node.is_deleted())
                print('Actual s: ' + str(self.head.s))
                print('old_s: ' + str(old_s))
                print('spl: ' + str(search_path_length))
                print('sp: ' + str(search_path2))
                self.print()
                exit()

        # Threshold rebalancing
        rebalances = 0
        self.update_longest_search_path(node)
        if self.rebalance_at_threshold:
            threshold = ceil(4 * self.height() * self.rebalance_threshold) - 1
            x = node.left()
            moved_left = True
            while x is not None and self.head.longest_search_path > threshold:
                if moved_left:
                    rebalances += self.remove_deleted_nodes_from_sublist(x)
                else:
                    rebalances += self.remove_deleted_nodes_from_sublist(x.r)
                rebalances += self.rebalance_sublist(x)

                if x.up is not None:
                    x = x.up
                    moved_left = False
                else:
                    x = x.left()
                    moved_left = True
            try:
                assert (self.head.longest_search_path <= threshold)
            except AssertionError:
                print('Delete. \nLongest search path: ' + str(self.head.longest_search_path))
                print('Threshold: ' + str(threshold))
                print('size: ' + str(self.size))
                self.print()
                exit()

        # Debug
        if self.debug:
            print('Delete: ' + str(key))

        return rebalances

    # endregion

    # region Rebalancing

    def full_rebalance(self):
        rebalances = 0
        while self.rebalance():
            rebalances += 1
            continue
        return rebalances

    def full_rebalance2(self):
        while self.rebalance2(self.head):
            continue

    def rebalance_sublist(self, node):
        rebalances = 0
        while self.rebalance2(node):
            rebalances += 1
        return rebalances

    def remove_deleted_nodes_from_sublist(self, node):
        rebalances = 0

        if node.is_tail() or node.is_bottom():
            return 0

        if node.r.up is None or node.r.is_deleted():
            assert(node.r is not node)
            rebalances += self.remove_deleted_nodes_from_sublist(node.r)

        if node.down is not self.bottom:
            rebalances += self.remove_deleted_nodes_from_sublist(node.down)

        while node.deleted_pointer_block is not None:
            self.remove_deleted_pointer_block(node.deleted_pointer_block)
            rebalances += 1
            node = node.down

        return rebalances

    def rebalance(self):
        if self.ub_conflicts is not None:
            self.rebalance_raise(self.ub_conflicts)
            return True
        if self.lb_conflicts is not None:
            self.rebalance_lb(self.lb_conflicts)
            return True
        if self.deleted_pointer_block is not None:
            self.remove_deleted_pointer_block(self.deleted_pointer_block)
            return True
        return False

    def rebalance2(self, node):
        x = self.find_conflict(node)

        if x.deleted_pointer_block is not None:
            self.remove_deleted_pointer_block(x.deleted_pointer_block)
            return True
        elif x.lb_conflict_right is not None:
            assert(x is not node)
            self.rebalance_lb(x.lb_conflict_right)
            return True
        elif x.ub_conflict is not None:
            self.rebalance_raise(x.ub_conflict)
            return True

        x.possible_conflict = False
        return False

    def find_conflict(self, node):
        if not node.possible_conflict:
            return node

        x = self.find_possible_conflict_node(node)
        while x.has_no_conflict() and x is not node:
            x = self.find_possible_conflict_node(node)
        return x

    def find_possible_conflict_node(self, node):
        result = None
        if node.down.possible_conflict and node.r.possible_conflict and node.r.is_not_tail() and node.r.height() <= node.height():
            if randint(0, 1) > 0:
                result = self.find_possible_conflict_node(node.down)
            else:
                result = self.find_possible_conflict_node(node.r)
        elif node.down.possible_conflict:
            result = self.find_possible_conflict_node(node.down)
        elif node.r.possible_conflict and node.r.is_not_tail() and node.r.height() <= node.height():
            result = self.find_possible_conflict_node(node.r)

        if result is None:
            node.possible_conflict = False
            return node

        return result

    def rebalance_raise(self, conflict):
        old_k = self.head.k
        self.delete_ub_conflict(conflict)
        node = conflict.node
        x = node
        for i in range(self.ub):
            x = x.right()
        x.k -= 1

        new_node = x.increment_height(None, None)
        if new_node.height() > self.head.height():
            self.head = self.head.increment_height(None, new_node)
            self.tail = self.tail.increment_height(new_node, None)
            new_node.l = self.head
            new_node.r = self.tail
            self.head.possible_conflict = True
        else:
            left = x.l
            while left.up is None and left.is_not_head():
                left = left.l
            right = x.r
            while right.up is None and right.is_not_tail():
                right = right.r
            new_node.l = left.up
            new_node.r = right.up
            right.up.l = new_node
            left.up.r = new_node

            # Remove eventual LB conflict
            self.delete_lb_conflict(new_node.left().lb_conflict_right)
            self.delete_lb_conflict(new_node.right().lb_conflict_left)

            # Check for UB conflict
            self.cuc(new_node)
        self.cuc(x.right(), True)

        # Remove eventual LB conflicts below
        if node.down.lb_conflict_left is not None:
            self.delete_lb_conflict(node.down.lb_conflict_left)
            self.clc_left(node.down, node.height() - 2)
        if node.down.lb_conflict_right is not None:
            self.delete_lb_conflict(node.down.lb_conflict_right)
            self.clc_right(node.down, node.height() - 2)

        # Conflict Trace
        new_node.possible_conflict = True

        # Decorate
        if self.decorate:
            self.decorate_after_raise(new_node)
            try:
                assert(old_k == self.head.k)
            except AssertionError:
                print('Raise:' + str(node.key()))
                print('Excepted k-value:' + str(old_k) + ', Actual k-value: ' + str(self.head.k))
                self.print()
                exit()

        # Longest search path decoration
        new_node.down.update_longest_search_path()
        new_node.update_longest_search_path()
        self.update_longest_search_path(new_node.down.l)

        if self.debug:
            print('Raise:' + str(x.key()))
            self.print()

    def rebalance_lb(self, conflict):
        rsize = 0
        lsize = 0
        x = conflict.right.right()
        if x is not None and conflict.right.up.up is None:
            while x.up is None and x.is_not_tail() and rsize < 3:
                x = x.right()
                rsize += 1
        x = conflict.left.left()
        if x is not None and conflict.left.up.up is None:
            while x.up is None and x.is_not_head() and lsize < 3:
                x = x.left()
                lsize += 1
        if rsize == 3:
            self.slide(conflict.right.right().right(), conflict.right)
        elif lsize == 3:
            self.slide(conflict.left.left().left(), conflict.left)
        elif rsize == 2:
            self.slide(conflict.right.right(), conflict.right)
        elif lsize == 2:
            self.slide(conflict.left.left(), conflict.left)
        elif conflict.left.up.up is None and conflict.left.is_not_head():
            self.lower(conflict.left)
        elif conflict.right.up.up is None and conflict.right.is_not_tail():
            self.lower(conflict.right)
        else:
            self.print()
            print(conflict)
            raise Exception("Invalid conflict attempted solved")

    def lower(self, node):
        old_k = self.head.k
        node_up = node.up
        left = node_up.left()
        right = node_up.left()
        lower_head_and_tail = node_up.l is self.head and node_up.r is self.tail and self.head.height() > 1

        if lower_head_and_tail:
            self.head = self.head.down
            self.head.up = None
            self.head.decr_height()
            self.tail = self.tail.down
            self.tail.up = None
            self.tail.decr_height()
        else:
            node_up.r.l = node_up.l
            node_up.l.r = node_up.r
        node.decr_height()
        node.up = None

        # Conflict checking
        if left.up is None:
            self.cuc(left)
        elif right.up is None:
            self.cuc(right)

        self.delete_lb_conflict(node.lb_conflict_left)
        self.delete_lb_conflict(node.lb_conflict_right)

        if node.height() > 1:
            self.clc_left(node.down, node.height() - 1)
            self.clc_right(node.down, node.height() - 1)

        if node.left().up is not None:
            self.clc_right(node.left().up, node.height() + 1)
        elif node.right().up is not None:
            self.clc_left(node.right().up, node.height() + 1)

        # Conflict Trace
        node.possible_conflict = True
        x = node.l
        while x is not None and x.up is None:
            x.possible_conflict = True
            x = x.l

        # Decorate
        if self.decorate:
            node.update_decoration()
            x = node.l
            while x.up is not None or x.l is not None:
                x.update_decoration()
                if x.up is None:
                    x = x.l
                else:
                    x = x.up
            x.update_decoration()

            try:
                assert(old_k == self.head.k)
            except AssertionError:
                print('Lower:' + str(node.key()))
                print('Excepted k-value:' + str(old_k) + ', Actual k-value: ' + str(self.head.k))
                self.print()
                exit()

        # Longest search path decoration
        self.update_longest_search_path(node)

        if self.debug:
            print('Lower:' + str(node.key()))
            self.print()

    def slide(self, destination_node, node_to_slide):
        assert(destination_node.is_not_head() and destination_node.is_not_tail())
        assert(node_to_slide.is_not_head() and node_to_slide.is_not_tail())

        left = destination_node.l
        while left.up is None and left.is_not_head():
            left = left.l
        right = destination_node.r
        while right.up is None and right.is_not_tail():
            right = right.r
        destination_node.up = Node(destination_node.info, self, right.up, left.up, destination_node)
        right.up.l = destination_node.up
        left.up.r = destination_node.up
        destination_node.incr_height()
        destination_node.up.possible_conflict = True

        node_to_slide.up.l.r = node_to_slide.up.r
        node_to_slide.up.r.l = node_to_slide.up.l
        node_to_slide.decr_height()
        node_to_slide.up = None

        # Determine slide direction
        right_slide = node_to_slide.key() > destination_node.key()

        # Conflict checking
        self.delete_lb_conflict(node_to_slide.lb_conflict_left)
        self.delete_lb_conflict(node_to_slide.lb_conflict_right)

        if node_to_slide.height() > 1:
            self.clc_left(node_to_slide.down, node_to_slide.height() - 1)
            self.clc_right(node_to_slide.down, node_to_slide.height() - 1)

        self.delete_ub_conflict(node_to_slide.ub_conflict)
        if right_slide:
            self.cuc(destination_node.left())
        else:
            self.cuc(destination_node.right())

        if destination_node.down.lb_conflict_left is not None:
            self.delete_lb_conflict(destination_node.down.lb_conflict_left)
            self.clc_left(destination_node.down, destination_node.height() - 2)
        if destination_node.down.lb_conflict_right is not None:
            self.delete_lb_conflict(destination_node.down.lb_conflict_right)
            self.clc_right(destination_node.down, destination_node.height() - 2)

        # Decorate
        if self.decorate:
            old_k = self.head.k
            if right_slide:
                x = node_to_slide
                while x is not destination_node:
                    x.update_decoration()
                    up = x.up
                    while up is not None:
                        up.update_decoration()
                        up = up.up
                    x = x.l
            else:
                x = node_to_slide
                while x.up is not None or x.l is not None:
                    x.update_decoration()
                    if x.up is None:
                        x = x.l
                    else:
                        x = x.up
                x.update_decoration()
            destination_node.update_decoration()
            destination_node.up.update_decoration()
            x = destination_node.l
            while x.up is not None or x.l is not None:
                x.update_decoration()
                if x.up is None:
                    x = x.l
                else:
                    x = x.up
            x.update_decoration()
            try:
                assert(old_k == self.head.k)
            except AssertionError:
                print('Slide: ' + str(node_to_slide.key()) + ' -> ' + str(destination_node.key()))
                print('Excepted k-value:' + str(old_k) + ', Actual k-value: ' + str(self.head.k))
                self.print()
                exit()

        # Longest search path decoration
        destination_node.update_longest_search_path()
        destination_node.up.update_longest_search_path()
        self.update_longest_search_path(destination_node.l)

        if self.debug:
            print('Slide: ' + str(node_to_slide.key()) + ' -> ' + str(destination_node.key()))
            self.print()

    def remove_deleted_pointer_block(self, deleted_pointer_block):
        self.delete_deleted_pointer_block(deleted_pointer_block)
        node = deleted_pointer_block.node
        lower_head_and_tail = node.l is self.head and node.r is self.head and self.head.height > 1
        if node.is_deleted():
            if lower_head_and_tail:
                self.head = self.head.down
                self.head.up = None
                self.head.decr_height()
                self.tail = self.tail.down
                self.tail.up = None
                self.tail.decr_height()
            else:
                node.l.r = node.r
                node.r.l = node.l
            node.down.up = None
            node.decr_height()
            if not node.down.is_bottom():
                self.add_deleted_pointer_block(node.down)
        else:
            raise Exception("Trying to remove non deleted node.")

        # Decorate
        if self.decorate:
            old_k = self.head.k
            self.decorate_after_node_removal(node)
            try:
                assert(old_k == self.head.k)
            except AssertionError:
                print('Remove: ' + str(node.key()))
                print(old_k)
                print(self.head.k)
                print(node.key())
                self.print()
                exit()

        # Conflict Trace
        if not node.down.is_bottom():
            node.down.possible_conflict = True
            x = node.down.l
            while x.up is None:
                x.possible_conflict = True
                x = x.l
            x.possible_conflict = True

        # Longest search path decoration
        if not node.down.is_bottom():
            self.update_longest_search_path(node.down)
        else:
            self.update_longest_search_path(node.l)

        if self.debug:
            print('Remove: ' + str(node.key()))
            self.print()

    # endregion

    # region Conflicts

    def cuc(self, node, new=False):
        x = node
        size = 0
        while x is not None and x.up is None and x.is_not_head() and size < self.ub + 2:
            size += 1
            x = x.left()
        l = x
        x = node.right()
        while x is not None and x.up is None and x.is_not_tail() and size < self.ub + 2:
            size += 1
            x = x.right()

        if size == self.ub + 1 or (size > self.ub and new):
            if l.ub_conflict is None:
                self.add_ub_conflict(UpperBoundConflict(l))

                # Conflict Trace
                x = l
                while (x.up is not None or x.l is not None) and not x.possible_conflict:
                    x.possible_conflict = True
                    if x.up is None:
                        x = x.l
                    else:
                        x = x.up
                x.possible_conflict = True

        if size <= self.ub:
            self.delete_ub_conflict(l.ub_conflict)

    def add_ub_conflict(self, conflict):
        if self.ub_conflicts is None:
            self.ub_conflicts = conflict
        else:
            conflict.previous = self.next_ub_conflict
            self.next_ub_conflict.next = conflict
        self.next_ub_conflict = conflict

    def delete_ub_conflict(self, conflict):
        if conflict is not None:
            conflict.node.ub_conflict = None

            if conflict is self.ub_conflicts and conflict is self.next_ub_conflict:
                self.ub_conflicts = None
                self.next_ub_conflict = None
            elif conflict is self.ub_conflicts:
                self.ub_conflicts = self.ub_conflicts.next
                self.ub_conflicts.previous = None
            elif conflict is self.next_ub_conflict:
                self.next_ub_conflict = self.next_ub_conflict.previous
                self.next_ub_conflict.next = None
            else:
                conflict.previous.next = conflict.next
                conflict.next.previous = conflict.previous

    def clc_left(self, node, conflict_height):
        left = node.left()
        assert(not node.is_deleted())
        assert(not left.is_deleted())
        self.delete_lb_conflict(node.lb_conflict_left)
        self.delete_lb_conflict(left.lb_conflict_right)
        if node.height() > conflict_height and left.height() > conflict_height:
            if node.height() - conflict_height == 1 or left.height() - conflict_height == 1:
                self.add_lb_conflict(LowerBoundConflict(left, node))
                self.update_possible_conflict(left)
                if node.is_not_tail():
                    self.update_possible_conflict(node)
                assert(node.height() > 1 and left.height() > 1)
                return True
        return False

    def clc_right(self, node, conflict_height):
        right = node.right()
        assert(not node.is_deleted())
        assert(not right.is_deleted())
        self.delete_lb_conflict(node.lb_conflict_right)
        self.delete_lb_conflict(right.lb_conflict_left)
        if node.height() > conflict_height and right.height() > conflict_height:
            if node.height() - conflict_height == 1 or right.height() - conflict_height == 1:
                self.add_lb_conflict(LowerBoundConflict(node, right))
                self.update_possible_conflict(node)
                if right.is_not_tail():
                    self.update_possible_conflict(right)
                assert(node.height() > 1 and right.height() > 1)
                return True
        return False

    def add_lb_conflict(self, conflict):
        if self.lb_conflicts is None:
            self.lb_conflicts = conflict
        else:
            conflict.previous = self.next_lb_conflict
            self.next_lb_conflict.next = conflict
        self.next_lb_conflict = conflict

    def delete_lb_conflict(self, conflict):
        if conflict is not None:
            conflict.left.lb_conflict_right = None
            conflict.right.lb_conflict_left = None

            if conflict is self.lb_conflicts and conflict is self.next_lb_conflict:
                self.lb_conflicts = None
                self.next_lb_conflict = None
            elif conflict is self.lb_conflicts:
                self.lb_conflicts = self.lb_conflicts.next
                self.lb_conflicts.previous = None
            elif conflict is self.next_lb_conflict:
                self.next_lb_conflict = self.next_lb_conflict.previous
                self.next_lb_conflict.next = None
            else:
                conflict.previous.next = conflict.next
                conflict.next.previous = conflict.previous

    def add_deleted_pointer_block(self, node):
        pointer_block = DeletedPointerBlock(node)
        if self.deleted_pointer_block is None:
            self.deleted_pointer_block = pointer_block
        else:
            pointer_block.previous = self.next_deleted_pointer_block
            self.next_deleted_pointer_block.next = pointer_block
        self.next_deleted_pointer_block = pointer_block

    def delete_deleted_pointer_block(self, pointer_block):
        if pointer_block is not None:
            pointer_block.node.deleted_pointer_block = None

            if pointer_block is self.deleted_pointer_block and pointer_block is self.next_deleted_pointer_block:
                self.deleted_pointer_block = None
                self.next_deleted_pointer_block = None
            elif pointer_block is self.deleted_pointer_block:
                self.deleted_pointer_block = self.deleted_pointer_block.next
                self.deleted_pointer_block.previous = None
            elif pointer_block is self.next_deleted_pointer_block:
                self.next_deleted_pointer_block = self.next_deleted_pointer_block.previous
                self.next_deleted_pointer_block.next = None
            else:
                pointer_block.previous.next = pointer_block.next
                pointer_block.next.previous = pointer_block.previous

    # endregion

    # region Decoration

    def decorate_after_raise(self, node):
        node.update_decoration()
        x = node.down.l
        while x.up is not None or x.l is not None:
            x.update_decoration()
            if x.up is None:
                x = x.l
            else:
                x = x.up
        x.update_decoration()

    def decorate_after_node_removal(self, node):
        if node.down is not self.bottom:
            x = node.down
        else:
            x = node.l

        while x.up is not None or x.l is not None:
            x.update_decoration()
            if x.up is None:
                x = x.l
            else:
                x = x.up
        x.update_decoration()

    def update_longest_search_path(self, node):
        x = node
        x.update_longest_search_path()
        while x.up is not None or x.l is not None:
            x.update_longest_search_path()
            if x.up is None:
                x = x.l
            else:
                x = x.up
        x.update_longest_search_path()

    def update_possible_conflict(self, node):
        x = node
        x.possible_conflict = True
        while x.up is not None or x.l is not None and not x.possible_conflict:
            x.possible_conflict = True
            if x.up is None:
                x = x.l
            else:
                x = x.up
        x.possible_conflict = True

    # endregion

    def print(self):
        x = self.head
        while x.down is not self.bottom:
            x = x.down

        result = []
        while x is not None:
            y = x
            node_representation = []
            for i in range(self.head.height()):
                if y is not None:
                    node_representation.append('{:^10}'.format(str(y.longest_search_path) + ',' + str(int(y.possible_conflict))))
                    y = y.up
                else:
                    node_representation.append('          ')
            result.append(node_representation)
            x = x.r

        print('Content:')
        for i in reversed(range(self.head.height())):
            string = ''
            for e in result:
                string += e[i]
            print(string)

        x = self.head
        while x.down is not self.bottom:
            x = x.down
        while x is not None:
            if x.key() == -2147483647:
                print('{:^10}'.format('H'), end='')
            elif x.key() == 2147483647:
                print('{:^10}'.format('T'), end='')
            elif x.is_deleted():
                print('{:^10}'.format('(' + str(round(x.key(), 1)) + ')'), end='')
            else:
                print('{:^10}'.format(str(round(x.key(), 1))), end='')
            x = x.r
        print('')
        print('UB Conflicts: ', end='')
        x = self.ub_conflicts
        while x is not None:
            print(x, end=' -> ')
            x = x.next
        print('')
        print('LB Conflicts: ', end='')
        x = self.lb_conflicts
        while x is not None:
            print(x, end=' -> ')
            x = x.next
        print('\n')

if __name__ == "__main__":
    from random import *

    def test_inserts_in_one_gap():
        skiplist = SkipList(3)
        for i in range(1, 1001):
            skiplist.insert(i)
        skiplist.full_rebalance()

        search_lengths = [0] * 25
        for i in range(1, 1001):
            l = skiplist.measure_search_path_length_all(i)
            search_lengths[l] += 1

        for i, e in enumerate(search_lengths):
            print(str(e))
        skiplist.print()


    def test_decoration():
        def new_skiplist(size):
            sl = SkipList(3)
            for k in range(1, size + 1):
                sl.insert(k)
            sl.full_rebalance()
            return sl

        # Build initial list
        skiplist = SkipList(3)
        for i in range(1, 14):
            skiplist.insert(i)

        assert(skiplist.head.s == 91)
        assert(skiplist.head.k == 14)

        # Rebalance
        while skiplist.rebalance():
            continue

        assert(skiplist.head.s == 50)
        assert(skiplist.head.k == 14)

        # Test deletion
        skiplist.delete(8)
        skiplist.delete(9)

        assert(skiplist.head.s == 43)
        assert(skiplist.head.k == 12)

        # Rebalance
        while skiplist.rebalance():
            continue

        assert(skiplist.head.s == 49)
        assert(skiplist.head.k == 12)

        # Restore to initial list
        skiplist.insert(8)
        skiplist.insert(9)

        assert(skiplist.head.s == 66)
        assert(skiplist.head.k == 14)

        while skiplist.rebalance():
            continue

        assert(skiplist.head.s == 50)
        assert(skiplist.head.k == 14)

        # Test lower left side
        for i in (2, 5, 7, 8, 11):
            skiplist.delete(i)

        skiplist.rebalance()

        assert(skiplist.head.s == 28)
        assert(skiplist.head.k == 9)

        # Test lower right side
        skiplist = new_skiplist(13)
        for i in (10, 11):
            skiplist.delete(i)

        skiplist.rebalance()

        assert(skiplist.head.s == 46)
        assert(skiplist.head.k == 12)

        # Test borrow 1 from right
        skiplist = new_skiplist(13)
        for i in (1, 2):
            skiplist.delete(i)

        skiplist.rebalance()

        assert(skiplist.head.s == 43)
        assert(skiplist.head.k == 12)

        # Test borrow 1 from left
        skiplist = new_skiplist(13)
        for i in (4, 5, 6, 7, 8):
            skiplist.delete(i)

        skiplist.rebalance()

        assert(skiplist.head.s == 27)
        assert(skiplist.head.k == 9)

        # Test borrow 2 from right
        skiplist = new_skiplist(13)
        for i in (1, 2, 6):
            skiplist.delete(i)

        skiplist.rebalance_lb(skiplist.lb_conflicts)

        assert(skiplist.head.s == 42)
        assert(skiplist.head.k == 11)

        # Test borrow 2 from left
        skiplist = new_skiplist(13)
        for i in (3, 7, 8):
            skiplist.delete(i)

        skiplist.rebalance_lb(skiplist.lb_conflicts)

        assert(skiplist.head.s == 39)
        assert(skiplist.head.k == 11)

    def test():
        skiplist = SkipList(3)
        skiplist.insert(1)
        skiplist.insert(2)
        skiplist.insert(3)
        skiplist.insert(4)
        skiplist.insert(5)
        skiplist.insert(6)
        skiplist.insert(7)
        skiplist.insert(8)
        skiplist.insert(9)
        skiplist.insert(10)
        skiplist.insert(11)
        skiplist.insert(12)
        skiplist.insert(13)
        skiplist.full_rebalance2()
        skiplist.delete(11)
        skiplist.print()
        skiplist.full_rebalance2()
        skiplist.print()
        skiplist.delete(10)
        print('Delete: 10')
        skiplist.print()
        print('1: Rebalance after delete: 10')
        skiplist.rebalance2(skiplist.head)
        skiplist.print()
        print('2: Rebalance after delete: 10')
        skiplist.rebalance2(skiplist.head)
        skiplist.print()
        print('3: Rebalance after delete: 10')
        skiplist.rebalance2(skiplist.head)
        skiplist.print()
        skiplist.delete(6)
        print('Delete: 6')
        skiplist.print()
        skiplist.rebalance2(skiplist.head)
        skiplist.print()
        skiplist.rebalance2(skiplist.head)
        skiplist.print()
        skiplist.rebalance2(skiplist.head)
        skiplist.print()
        skiplist.rebalance2(skiplist.head)
        skiplist.print()
        skiplist.rebalance2(skiplist.head)
        skiplist.print()

    def test2():
        skiplist = SkipList(3)
        for i in range(1, 25):
            skiplist.insert(i)
        skiplist.full_rebalance()
        skiplist.delete(13)
        skiplist.delete(14)
        skiplist.rebalance()
        skiplist.rebalance()
        skiplist.print()

    test_inserts_in_one_gap()


