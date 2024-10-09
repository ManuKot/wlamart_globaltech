class PowerOfTwoMaxHeap {
    constructor(childrenFactor) {
        this.childrenFactor = childrenFactor;
        this.heap = [];
    }

    insert(value) {
        this.heap.push(value);
        this.bubbleUp(this.heap.length - 1);
    }

    popMax() {
        if (this.heap.length === 0) return null;

        const maxValue = this.heap[0];
        const lastValue = this.heap.pop();
        if (this.heap.length > 0) {
            this.heap[0] = lastValue;
            this.bubbleDown(0);
        }
        return maxValue;
    }

    bubbleUp(index) {
        const parentIndex = Math.floor((index - 1) / Math.pow(2, this.childrenFactor));
        while (index > 0 && this.heap[index] > this.heap[parentIndex]) {
            [this.heap[index], this.heap[parentIndex]] = [this.heap[parentIndex], this.heap[index]];
            index = parentIndex;
        }
    }

    bubbleDown(index) {
        const length = this.heap.length;
        while (true) {
            let largest = index;
            for (let i = 0; i < Math.pow(2, this.childrenFactor); i++) {
                const childIndex = Math.pow(2, this.childrenFactor) * index + i + 1;
                if (childIndex < length && this.heap[childIndex] > this.heap[largest]) {
                    largest = childIndex;
                }
            }
            if (largest === index) break;
            [this.heap[index], this.heap[largest]] = [this.heap[largest], this.heap[index]];
            index = largest;
        }
    }
}

// Testing the JavaScript implementation
const heap = new PowerOfTwoMaxHeap(2); // Each parent has 4 children (2^2)
heap.insert(10);
heap.insert(20);
heap.insert(15);
heap.insert(30);

console.log(heap.popMax()); // Should output 30
console.log(heap.popMax()); // Should output 20
console.log(heap.popMax()); // Should output 15
console.log(heap.popMax()); // Should output 10
console.log(heap.popMax()); // Should output null (heap is empty)
