# Review 1
def add_to_list(value, my_list=[]):
    my_list.append(value)
    return my_list

"""
The issue for add_to_list above is initializing the parameter my_list with empty list in the argument. 
We may encounter unexpected results after adding elements into the original list.
For example, my_list will be [1] after we call add_to_list(1) initially. Then it will be [1,2] 
after we call add_to_list(2) which may not be the exact result from the caller.
To solve this, we should initialize my_list with None and create an empty list in the function.
"""
def add_to_list_revised(value, my_list=None): # modified
    if not my_list: # added
        my_list = [] # added
    my_list.append(value)
    return my_list
 
# Review 2
def format_greeting(name, age):
    return "Hello, my name is {name} and I am {age} years old."

"""
We should use f-string in format_greeting to refer variables, otherwise the values of name and age will not
be passed to the return string.
"""
def format_greeting_revised(name, age):
    return f"Hello, my name is {name} and I am {age} years old." # modified
 
# Review 3
class Counter:
    count = 0
    def __init__(self):
        self.count += 1
    def get_count(self):
        return self.count

"""
In the Counter class above, self.count is in instance namespace wile count=0 is in class namespace. 
As a result, the method get_count always returns 1 when we create new objects for this class which 
is not going to increasing the value of count in class scope.
To solve this, count namespace should be set to class namespace instead of instance namespace.
"""
class CounterRevised:
    count = 0
    def __init__(self):
        self.__class__.count += 1 # modified
    def get_count(self):
        return self.__class__.count # modified
 
# Review 4
import threading
class SafeCounter:
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count += 1
 
def worker(counter):
    for _ in range(1000):
        counter.increment()
 
counter = SafeCounter()
threads = []
for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)
 
for t in threads:
    t.join()

"""
The problem for the program above is that no synchronization mechanism was added for class SafeCounter
which may cause potential issues during multiple threads' modifying self.count.
It will be safe after we add thread lock for controlling the writing operations from different threads.
"""
class SafeCounterRevised:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock() # added
    def increment(self):
        with self.lock: # added
            self.count += 1
 
# Review 5
def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] =+ 1
        else:
            counts[item] = 1
    return counts

"""
In the function above, obviously there is a syntax issue in Line 91 for '=+' which assigns 1 to 
counts[item] all the time. With this problem, the occurrences for an existing item in the dictionary
will always equal to 1 which is not the intended functionality.
To solve this, we must change '=+' to '+='.
Besides that, we need to add an exception handler if there is a mutable object in the list. If so,
such exception will be ignored and will not break the execution.
"""
def count_occurrences_revised(lst):
    counts = {}
    for item in lst:
        try:
            if item in counts:
                counts[item] += 1 # modified
            else:
                counts[item] = 1
        except TypeError: # added for defense of mutable objects
            continue
    return counts
