"""
Implement the myReduceRight method. This is similar to myReduce, with the difference that
it calls the reducer function fn from the end of the list to the beginning. For example,
if the list is cons(1, cons(2, cons(3))), myReduceRight(fn, accm, list) should return
the result of evaluating fn(1, fn(2, fn(3, accm))).

Here we use recursion to achieve this goal.
Base case: the linked list is exhausted.
Procedures: In each recursion, the linked list's head is the first argument of fn, while the
rest part is the third argument of myReduceRight.

Let's take linked list 1->2->3 as an example,
Call Stack:
***TOP***
myReduceRight(fn, accm, None)       -> accm
myReduceRight(fn, accm, 3)          -> fn(1, fn(2, fn(3, myReduceRight(fn, accm, None))))
myReduceRight(fn, accm, 2->3)       -> fn(1, fn(2, myReduceRight(fn, accm, 3)))
myReduceRight(fn, accm, 1->2->3)    -> fn(1, myReduceRight(fn, accm, 2->3))
**BOTTOM**

As a result, the final return value for myReduceRight is fn(1, fn(2, fn(3, accm))) as expected.
"""


def llToArray(ll):
    if not ll:
        return None

    values = []
    temp = ll.head
    while temp:
        values.append(temp.value)
        temp = temp.next
    return values


def myReduceRight(fn, accm, array):
    if not array:
        return accm
    return fn(array[0], myReduceRight(fn, accm, array[1:]))


# Test
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def print_list(self):
        temp = self.head
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def append(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1
        return True


my_ll = LinkedList(1)
my_ll.append(2)
my_ll.append(3)
my_ll.append(4)
print("Original linked list is:")
my_ll.print_list()
print("========================\n")

my_ll1 = LinkedList(1)
my_ll1.append(2)
my_ll1.append(3)
my_ll1.append(4)


def unfoldCalculation(a, b):
    return "fn(" + str(a) + ", " + str(b) + ")"


def xTimesTwoPlusY(x, y):
    return x * 2 + y


def printXAndReturnY(x, y):
    print(x)
    return y


print(
    "unfoldCalculation for a function recursively: ",
    myReduceRight(unfoldCalculation, "accm", llToArray(my_ll)),
)
print(
    "------------------------------------------------------------------------------------"
)
print(
    "xTimesTwoPlusY after recursion: ",
    myReduceRight(xTimesTwoPlusY, 0, llToArray(my_ll)),
)
print(
    "------------------------------------------------------------------------------------"
)
print("The list after executing printXAndReturnY recursively:")
print(myReduceRight(printXAndReturnY, 0, llToArray(my_ll)))
print(
    "------------------------------------------------------------------------------------"
)
