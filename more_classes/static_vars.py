

class Counter:
    count = 0  

    def __init__(self):
        Counter.count += 1

    @staticmethod
    def get_count():
        return Counter.count

if __name__ == '__main__':
    a = Counter()
    b = Counter()
    c = Counter()
    print("Instances created:", Counter.get_count())
