#Again, the core of the way I did the schduling was letting the min-heap have control
#It sorts itself based on the process.value which can have multiple meaning depending on the algorithm*
#Another interesing property is it naturally defaults to first come first serve if there is a tie because it was placed in the min-heap first
class MinHeap:
    def __init__(self):
        self.Heap = []
    def isEmpty(self):
        return len(self.Heap) == 0
    def peek(self):
        return self.Heap[0]
    def pullUp(self, index):
        parentIndex = int((index - 1) / 2)
        if self.Heap[index].value < self.Heap[parentIndex].value:
            Temp = self.Heap[index]
            self.Heap[index] = self.Heap[parentIndex]
            self.Heap[parentIndex] = Temp
            self.pullUp(parentIndex)
    def pushDown(self, index):
        LeftChild = 2 * index + 1
        RightChild = 2 * index + 2
        if LeftChild <= len(self.Heap) - 1:
            minIndex = index if self.Heap[LeftChild].value > self.Heap[index].value else LeftChild
            if RightChild <= len(self.Heap) - 1:
                minIndex = minIndex if self.Heap[RightChild].value > self.Heap[minIndex].value else RightChild
            if not minIndex == index:
                Temp = self.Heap[index]
                self.Heap[index] = self.Heap[minIndex]
                self.Heap[minIndex] = Temp
                self.pushDown(minIndex)
    def add(self, Process):
        self.Heap.append(Process)
        self.pullUp(len(self.Heap) - 1)
    def pop(self):
        if len(self.Heap) > 1:
            P = self.Heap[0]
            self.Heap[0] = self.Heap.pop()
            self.pushDown(0)
        else:
            P = self.Heap.pop()
        return P
