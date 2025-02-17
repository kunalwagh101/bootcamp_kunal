

from functools import total_ordering

@total_ordering
class ComparableItem:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if isinstance(other, ComparableItem):
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ComparableItem):
            return self.value < other.value
        return NotImplemented

    def __str__(self):
        return f"ComparableItem({self.value})"

if __name__ == '__main__':
    item1 = ComparableItem(10)
    item2 = ComparableItem(20)
    item3 = ComparableItem(10)

    print(item1 == item3) 
    print(item1 < item2)   
    print(item2 > item1)   
    print(item1 <= item3) 
