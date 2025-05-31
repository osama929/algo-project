import tkinter as tk
import time
import sys
import random
from functools import wraps

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=800, height=400, bg='white', bd=0, highlightthickness=1, relief='ridge')
        self.canvas.pack(pady=10)

        self.data = []

        # Title Label
        title = tk.Label(root, text="Sorting Algorithm Visualizer", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=10)

        # Input Frame
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Enter number of bars:", font=("Arial", 11), bg="#f0f0f0").grid(row=0, column=0, padx=5)
        self.entry = tk.Entry(input_frame, width=20, font=("Arial", 11))
        self.entry.grid(row=0, column=1, padx=5)
        self.entry.bind("<Return>", lambda event: self.generate_random_data())  # Bind Enter key

        tk.Button(input_frame, text="Generate Bars", command=self.generate_random_data, font=("Arial", 10), bg="#4CAF50", fg="white", width=15).grid(row=0, column=2, padx=5)

        # Button Frame
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        self.timed_bubble_sort = self.measure_performance(self.bubble_sort)
        self.timed_merge_sort = self.measure_performance(lambda: self.merge_sort(self.data, 0, len(self.data) - 1))
        self.timed_quick_sort = self.measure_performance(lambda: self.quick_sort(self.data, 0, len(self.data) - 1))

        tk.Button(btn_frame, text="Bubble Sort", command=self.timed_bubble_sort,
                  font=("Arial", 10), bg="#2196F3", fg="white", width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Merge Sort", command=self.timed_merge_sort,
                  font=("Arial", 10), bg="#9C27B0", fg="white", width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Quick Sort", command=self.timed_quick_sort,
                  font=("Arial", 10), bg="#FF5722", fg="white", width=15).pack(side=tk.LEFT, padx=10)

        # Metrics Frame
        self.metrics_frame = tk.Frame(root, bg="#f0f0f0")
        self.metrics_frame.pack(pady=10)

        self.time_label = tk.Label(self.metrics_frame, text="Time: -", font=("Arial", 11), bg="#f0f0f0")
        self.time_label.pack(side=tk.LEFT, padx=10)

        self.space_label = tk.Label(self.metrics_frame, text="Space: -", font=("Arial", 11), bg="#f0f0f0")
        self.space_label.pack(side=tk.LEFT, padx=10)

        tk.Button(self.metrics_frame, text="Reset Metrics", command=self.reset_metrics,
                  font=("Arial", 10), bg="#607D8B", fg="white", width=15).pack(side=tk.LEFT, padx=10)

    def reset_metrics(self):
        self.time_label.config(text="Time: -")
        self.space_label.config(text="Space: -")

    def measure_performance(self, func):
        @wraps(func)
        def wrapper():
            start_time = time.time()
            func()
            elapsed_time = time.time() - start_time

            base_size = sys.getsizeof(self.data)
            elements_size = sum(sys.getsizeof(x) for x in self.data)
            total_size = base_size + elements_size

            self.time_label.config(text=f"Time: {elapsed_time:.4f} seconds")
            self.space_label.config(text=f"Space: {total_size / 1024:.2f} KB")
        return wrapper

    def generate_random_data(self):
        try:
            num_bars = int(self.entry.get())
            if num_bars <= 0:
                raise ValueError
            self.data = [random.randint(10, 100) for _ in range(num_bars)]
            self.draw_bars(self.data)
        except ValueError:
            self.data = []
            self.draw_bars([])

    def draw_bars(self, data, color_array=None):
        self.canvas.delete("all")
        c_height = 400
        c_width = 800
        x_width = c_width / max(len(data), 1)
        spacing = 2
        normalized_data = [i / max(data) for i in data] if data else []
        for i, height in enumerate(normalized_data):
            x0 = i * x_width + spacing
            y0 = c_height - height * 350
            x1 = (i + 1) * x_width - spacing
            y1 = c_height
            color = color_array[i] if color_array else '#00bcd4'
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            self.canvas.create_text(x0 + 2, y0, anchor=tk.SW, text=str(self.data[i]), font=("Arial", 9))
        self.root.update_idletasks()

    def bubble_sort(self):
        data = self.data
        for i in range(len(data)):
            for j in range(len(data) - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                self.draw_bars(data, ['red' if x == j or x == j + 1 else '#00bcd4' for x in range(len(data))])
                time.sleep(0.1)

    def merge_sort(self, data, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(data, left, mid)
            self.merge_sort(data, mid + 1, right)
            self.merge(data, left, mid, right)
            self.draw_bars(data, ['green' if left <= x <= right else '#00bcd4' for x in range(len(data))])
            time.sleep(0.1)

    def merge(self, data, left, mid, right):
        left_part = data[left:mid + 1]
        right_part = data[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                data[k] = left_part[i]
                i += 1
            else:
                data[k] = right_part[j]
                j += 1
            k += 1
        while i < len(left_part):
            data[k] = left_part[i]
            i += 1
            k += 1
        while j < len(right_part):
            data[k] = right_part[j]
            j += 1
            k += 1

    def quick_sort(self, data, low, high):
        if low < high:
            pi = self.partition(data, low, high)
            self.draw_bars(data, ['purple' if x == pi else '#00bcd4' for x in range(len(data))])
            time.sleep(0.1)
            self.quick_sort(data, low, pi - 1)
            self.quick_sort(data, pi + 1, high)

    def partition(self, data, low, high):
        pivot = data[high]
        i = low - 1
        for j in range(low, high):
            if data[j] < pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                self.draw_bars(data, ['red' if x == i or x == j else '#00bcd4' for x in range(len(data))])
                time.sleep(0.1)
        data[i + 1], data[high] = data[high], data[i + 1]
        return i + 1

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
