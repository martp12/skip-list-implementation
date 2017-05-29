from SkipList import SkipList

# region Test Utilities

def new_skiplist(size, balance=False):
    sl = SkipList(3)
    for i in range(1, size + 1):
        sl.insert(i)
    if balance:
        sl.full_rebalance()
    return sl

# endregion

# region Insertion

def test_insert_in_3gap_causes_ub_conflict():
    skiplist = new_skiplist(3)
    assert(skiplist.ub_conflicts is None)
    skiplist.insert(4)
    assert(skiplist.ub_conflicts.node.key() == skiplist.head.key())

def test_insert_in_0gap_removes_lb_conflict():
    skiplist = new_skiplist(7, True)
    skiplist.delete(4)
    skiplist.delete(5)
    assert(skiplist.lb_conflicts is not None)
    skiplist.insert(5)
    assert(skiplist.lb_conflicts is None)

def test_insert_in_0gap_1gap_2gap_causes_no_ub_conflict():
    skiplist = new_skiplist(0)
    assert(skiplist.ub_conflicts is None)
    skiplist.insert(1)
    assert(skiplist.ub_conflicts is None)
    skiplist.insert(2)
    assert(skiplist.ub_conflicts is None)
    skiplist.insert(3)
    assert(skiplist.ub_conflicts is None)

def test_insert_in_4gap_causes_no_new_ub_conflict():
    skiplist = new_skiplist(4)
    assert(skiplist.ub_conflicts.node.key() == skiplist.head.key())
    assert(skiplist.ub_conflicts.next is None)
    skiplist.insert(5)
    assert(skiplist.ub_conflicts.node.key() == skiplist.head.key())
    assert(skiplist.ub_conflicts.next is None)

# endregion

# region Deletion

def test_delete_from_1gap_creates_lb_conflict():
    skiplist = new_skiplist(7, True)
    skiplist.delete(4)
    assert(skiplist.lb_conflicts is None)
    skiplist.delete(5)
    assert(skiplist.lb_conflicts.left.key() == 3)
    assert(skiplist.lb_conflicts.right.key() == 6)

def test_delete_from_2gap_3gap_creates_no_conflict():
    skiplist = new_skiplist(3)
    assert(skiplist.ub_conflicts is None)
    assert(skiplist.lb_conflicts is None)
    skiplist.delete(1)
    assert(skiplist.ub_conflicts is None)
    assert(skiplist.lb_conflicts is None)
    skiplist.delete(2)
    assert(skiplist.ub_conflicts is None)
    assert(skiplist.lb_conflicts is None)

def test_delete_from_4gap_removes_ub_conflict():
    skiplist = new_skiplist(4)
    assert(skiplist.ub_conflicts.node.key() == skiplist.head.key())
    skiplist.delete(3)
    assert(skiplist.ub_conflicts is None)

def test_delete_from_5gap_does_not_remove_ub_conflict():
    skiplist = new_skiplist(5)
    assert(skiplist.ub_conflicts.node.key() == skiplist.head.key())
    skiplist.delete(3)
    assert(skiplist.ub_conflicts.node.key() == skiplist.head.key())

#   endregion

# region Raise

def test_raise_4gap_5gap_6gap_remove_ub_conflict():
    skiplist = new_skiplist(4)
    assert(skiplist.ub_conflicts is not None)
    skiplist.rebalance_raise(skiplist.ub_conflicts)
    assert(skiplist.ub_conflicts is None)

    skiplist = new_skiplist(5)
    assert(skiplist.ub_conflicts is not None)
    skiplist.rebalance_raise(skiplist.ub_conflicts)
    assert(skiplist.ub_conflicts is None)

    skiplist = new_skiplist(6)
    assert(skiplist.ub_conflicts is not None)
    skiplist.rebalance_raise(skiplist.ub_conflicts)
    assert(skiplist.ub_conflicts is None)

def test_raise_7gap_moves_ub_conflict_to_raised_node():
    skiplist = new_skiplist(7)
    assert(skiplist.ub_conflicts.node.key() == skiplist.head.key())
    skiplist.rebalance_raise(skiplist.ub_conflicts)
    assert(skiplist.ub_conflicts.node.key() == 3)

def test_raise_ub_conflict_can_propagate_up():
    skiplist = new_skiplist(12)
    skiplist.delete(5)
    skiplist.delete(6)
    skiplist.full_rebalance()
    skiplist.insert(5)
    skiplist.insert(6)
    assert(skiplist.ub_conflicts.node.key() == 3)
    assert(skiplist.ub_conflicts.node.down is skiplist.bottom)
    assert(skiplist.ub_conflicts.next is None)
    skiplist.rebalance_raise(skiplist.ub_conflicts)
    assert(skiplist.ub_conflicts.node.key() == skiplist.head.key())
    assert(skiplist.ub_conflicts.node.down.down is skiplist.bottom)
    assert(skiplist.ub_conflicts.next is None)

def test_raise_does_not_propagate_conflict_up_to_gap_4gap():
    skiplist = new_skiplist(15)
    skiplist.delete(5)
    skiplist.delete(6)
    for i in range(4):
        skiplist.rebalance()
    skiplist.insert(5)
    skiplist.insert(6)
    assert(skiplist.ub_conflicts.next.node.key() == 3)
    assert(skiplist.ub_conflicts.node.key() == skiplist.head.key())
    skiplist.rebalance_raise(skiplist.ub_conflicts.next)
    assert(skiplist.ub_conflicts.node.key() == skiplist.head.key())
    assert(skiplist.ub_conflicts.next is None)

def test_raise_removes_lb_conflict_when_raised_into_0gap():
    skiplist = new_skiplist(22, True)
    for i in range(10, 18):
        skiplist.delete(i)
    for i in range(10,15):
        skiplist.insert(i)
    assert(skiplist.lb_conflicts is not None)
    skiplist.rebalance_raise(skiplist.ub_conflicts)
    assert(skiplist.lb_conflicts is None)

# endregion

# region Lower

def test_lower_removes_lb_conflict():
    skiplist = new_skiplist(4, True)
    skiplist.delete(1)
    skiplist.delete(2)
    assert(skiplist.lb_conflicts.right.key() == 3)
    skiplist.lower(skiplist.lb_conflicts.right)
    assert(skiplist.lb_conflicts is None)

def test_lower_can_discover_new_lb_conflicts_below():
    skiplist = new_skiplist(22, True)
    for i in range(1,9):
        skiplist.delete(i)
    for i in range(10,18):
        skiplist.delete(i)
    assert(skiplist.lb_conflicts.left.down.down is skiplist.bottom)
    assert(skiplist.lb_conflicts.next.left.down.down is skiplist.bottom)
    assert(skiplist.lb_conflicts.next.next is None)
    skiplist.lower(skiplist.lb_conflicts.right)
    assert(skiplist.lb_conflicts.left.down is skiplist.bottom)
    assert(skiplist.lb_conflicts.next.left.down is skiplist.bottom)
    assert(skiplist.lb_conflicts.next.next is None)

# endregion

#region Decoration

def test_decoration_raise_with_head_raise():
    skiplist = new_skiplist(10)
    assert(skiplist.head.k == 11)
    assert(skiplist.head.s == 55)
    skiplist.rebalance_raise(skiplist.ub_conflicts)
    assert(skiplist.head.k == 11)
    assert(skiplist.head.s == 48)

def test_decoration_raise_no_head_raise():
    skiplist = new_skiplist(13, True)
    skiplist.delete(6)
    assert(skiplist.head.k == 13)
    assert(skiplist.head.s == 47)
    skiplist.rebalance_raise(skiplist.ub_conflicts)
    assert(skiplist.head.k == 13)
    assert(skiplist.head.s == 46)

def test_decoration_raise_with_deleted_neighbor_of_same_height():
    skiplist = new_skiplist(10)
    skiplist.rebalance_raise(skiplist.ub_conflicts)
    skiplist.rebalance_raise(skiplist.ub_conflicts)
    skiplist.delete(6)
    assert(skiplist.head.k == 10)
    assert(skiplist.head.s == 35)
    skiplist.rebalance_raise(skiplist.ub_conflicts)
    assert(skiplist.head.k == 10)
    assert(skiplist.head.s == 34)

def test_decoration_lower_no_head_lower():
    skiplist = new_skiplist(13, True)
    skiplist.delete(2)
    skiplist.delete(4)
    skiplist.delete(5)
    skiplist.delete(7)
    assert(skiplist.head.k == 10)
    assert(skiplist.head.s == 32)
    skiplist.lower(skiplist.lb_conflicts.left)
    assert(skiplist.head.k == 10)
    assert(skiplist.head.s == 33)

def test_decoration_slide_1_forward():
    skiplist = new_skiplist(10, True)
    skiplist.delete(10)
    assert (skiplist.head.k == 10)
    assert (skiplist.head.s == 27)
    skiplist.rebalance_lb(skiplist.lb_conflicts)
    assert (skiplist.head.k == 10)
    assert (skiplist.head.s == 27)

def test_decoration_slide_2_forward():
    skiplist = new_skiplist(10, True)
    skiplist.delete(6)
    skiplist.delete(10)
    assert (skiplist.head.k == 9)
    assert (skiplist.head.s == 25)
    skiplist.rebalance_lb(skiplist.lb_conflicts)
    assert (skiplist.head.k == 9)
    assert (skiplist.head.s == 27)

def test_decoration_slide_1_backwards():
    skiplist = new_skiplist(10, True)
    skiplist.delete(1)
    skiplist.delete(2)
    assert (skiplist.head.k == 9)
    assert (skiplist.head.s == 27)
    skiplist.rebalance_lb(skiplist.lb_conflicts)
    assert (skiplist.head.k == 9)
    assert (skiplist.head.s == 27)

def test_decoration_slide_2_backwards():
    skiplist = new_skiplist(10, True)
    skiplist.delete(1)
    skiplist.delete(2)
    skiplist.delete(6)
    assert (skiplist.head.k == 8)
    assert (skiplist.head.s == 25)
    skiplist.rebalance_lb(skiplist.lb_conflicts)
    assert (skiplist.head.k == 8)
    assert (skiplist.head.s == 27)

#endregion

test_insert_in_0gap_1gap_2gap_causes_no_ub_conflict()
test_insert_in_0gap_removes_lb_conflict()
test_insert_in_3gap_causes_ub_conflict()
test_insert_in_4gap_causes_no_new_ub_conflict()

test_delete_from_1gap_creates_lb_conflict()
test_delete_from_2gap_3gap_creates_no_conflict()
test_delete_from_4gap_removes_ub_conflict()
test_delete_from_5gap_does_not_remove_ub_conflict()

test_raise_4gap_5gap_6gap_remove_ub_conflict()
test_raise_7gap_moves_ub_conflict_to_raised_node()
test_raise_ub_conflict_can_propagate_up()
test_raise_does_not_propagate_conflict_up_to_gap_4gap()
test_raise_removes_lb_conflict_when_raised_into_0gap()

test_lower_removes_lb_conflict()
test_lower_can_discover_new_lb_conflicts_below()

test_decoration_raise_with_head_raise()
test_decoration_raise_no_head_raise()
test_decoration_raise_with_deleted_neighbor_of_same_height()

test_decoration_lower_no_head_lower()

test_decoration_slide_1_forward()
test_decoration_slide_2_forward()
test_decoration_slide_1_backwards()
test_decoration_slide_2_backwards()