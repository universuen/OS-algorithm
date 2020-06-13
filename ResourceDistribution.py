import numpy as np

class Banker():
    def __init__(self, available:np.ndarray, max:np.ndarray, allocation:np.ndarray):
        self.shape = max.shape
        assert available.shape[0] == self.shape[1]
        assert allocation.shape == self.shape
        self.available = available
        self.max = max
        self.allocation = allocation
        self.need = max - allocation

    def request(self, requests:np.ndarray):
        result = []
        for i in range(self.shape[0]):
            if not self._less_or_equal(requests[i], self.need[i]):
                raise ValueError('Request should be less than or equal to Need')
            if not self._less_or_equal(requests[i], self.available):
                result.append(False)
                continue
            # 备份
            available = self.available.copy()
            allocation = self.allocation.copy()
            need = self.need.copy()
            # 试分配
            self.available -= requests[i]
            self.allocation[i] += requests[i]
            self.need[i] -= requests[i]
            # 安全性检查
            if self.is_safe():
                result.append(True)
            else:
                self.available = available
                self.allocation = allocation
                self.need = need
                result.append(False)
        return result

    def is_safe(self):
        work = self.available.copy()
        finish = [False for _ in range(self.shape[0])]
        exit = False
        sentence = []
        while not exit:
            exit = True
            for i in range(self.shape[0]):
                if finish[i] == False and self._less_or_equal(self.need[i], work):
                    work += self.allocation[i]
                    finish[i] = True
                    exit = False
                    sentence.append(i)
        # print(sentence)
        return not False in finish

    def _less_or_equal(self, a, b):
        for i, j in zip(a, b):
            if i > j:
                return False
        return True



if __name__ == '__main__':
    available = [3, 3, 2]
    available = np.asarray(available)

    max = [
        [8, 5, 3],
        [3, 2, 3],
        [9, 0, 3],
        [2, 2, 2],
        [5, 3, 3]
    ]
    max = np.asarray(max)

    allocation = [
        [1, 1, 0],
        [2, 0, 1],
        [3, 0, 3],
        [2, 1, 1],
        [1, 0, 2]
    ]
    allocation = np.asarray(allocation)

    banker = Banker(available, max, allocation)
    print(banker.is_safe())

    requests = [
        [0, 0, 0],
        [1, 0, 2],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    requests = np.asarray(requests)

    print(banker.request(requests))
