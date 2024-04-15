

class Utils:
    @staticmethod
    def add(tup1: tuple, tup2: tuple) -> list:
        lst1 = list(tup1)
        lst2 = list(tup2)
        res = [lst1[i] + lst2[i] for i in range(len(tup1))]
        return res
