import heapq
from typing import List

class SlidingMedian:
    def __init__(self):
        self.small = []  # max heap (store negatives)
        self.large = []  # min heap
        self.del_small = {}
        self.del_large = {}
        self.n_small = self.n_large = 0

    def _rebalance(self):
        if self.n_small > self.n_large + 1:
            val = -heapq.heappop(self.small)
            self.n_small -= 1
            heapq.heappush(self.large, val)
            self.n_large += 1
        elif self.n_small < self.n_large:
            val = heapq.heappop(self.large)
            self.n_large -= 1
            heapq.heappush(self.small, -val)
            self.n_small += 1

    def _clean_top(self, heap, del_map):
        while heap:
            v = -heap[0] if heap is self.small else heap[0]
            key = -heap[0] if heap is self.small else heap[0]
            if del_map.get(key,0):
                heapq.heappop(heap)
                del_map[key] -= 1
            else:
                break

    def add(self, num):
        if not self.small or num <= -self.small[0]:
            heapq.heappush(self.small, -num); self.n_small += 1
        else:
            heapq.heappush(self.large, num); self.n_large += 1
        self._rebalance()

    def remove(self, num):
        if self.small and num <= -self.small[0]:
            self.del_small[num] = self.del_small.get(num,0) + 1
            self.n_small -= 1
        else:
            self.del_large[num] = self.del_large.get(num,0) + 1
            self.n_large -= 1
        # clean tops
        while self.small and self.del_small.get(-self.small[0],0):
            val = -heapq.heappop(self.small)
            self.del_small[val] -= 1
        while self.large and self.del_large.get(self.large[0],0):
            val = heapq.heappop(self.large)
            self.del_large[val] -= 1
        self._rebalance()

    def median(self):
        if self.n_small + self.n_large == 0:
            return None
        if (self.n_small + self.n_large) % 2 == 1:
            # odd -> top of small
            while self.small and self.del_small.get(-self.small[0],0):
                val = -heapq.heappop(self.small)
                self.del_small[val] -= 1
            return -self.small[0]
        else:
            while self.small and self.del_small.get(-self.small[0],0):
                val = -heapq.heappop(self.small)
                self.del_small[val] -= 1
            while self.large and self.del_large.get(self.large[0],0):
                val = heapq.heappop(self.large)
                self.del_large[val] -= 1
            return (-self.small[0] + self.large[0]) / 2

def sliding_window_median(nums: List[int], k: int) -> List[float]:
    sm = SlidingMedian()
    res = []
    for i, val in enumerate(nums):
        sm.add(val)
        if i >= k:
            sm.remove(nums[i-k])
        if i >= k-1:
            res.append(sm.median())
    return res

# Example
if __name__ == "__main__":
    print(sliding_window_median([1,3,-1,-3,5,3,6,7], 3))  # [1, -1, -1, 3, 5, 6]
