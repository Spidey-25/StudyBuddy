/* Full source programs for the ten-minute typing activity. */
const STUDY_TYPING_PROGRAMS = {
  C: [
String.raw`#include <stdio.h>
#include <stdbool.h>

#define SIZE 6

void add_edge(int graph[SIZE][SIZE], int a, int b) {
    graph[a][b] = 1;
    graph[b][a] = 1;
}

void breadth_first_search(int graph[SIZE][SIZE], int start) {
    bool visited[SIZE] = { false };
    int queue[SIZE];
    int front = 0;
    int rear = 0;

    visited[start] = true;
    queue[rear++] = start;
    printf("BFS order:");

    while (front < rear) {
        int current = queue[front++];
        printf(" %d", current);

        for (int next = 0; next < SIZE; ++next) {
            if (graph[current][next] == 0) {
                continue;
            }
            if (visited[next]) {
                continue;
            }
            visited[next] = true;
            queue[rear++] = next;
        }
    }
    printf("\n");
}

int main(void) {
    int graph[SIZE][SIZE] = { { 0 } };
    add_edge(graph, 0, 1);
    add_edge(graph, 0, 2);
    add_edge(graph, 1, 3);
    add_edge(graph, 2, 3);
    add_edge(graph, 3, 4);
    add_edge(graph, 4, 5);

    printf("Graph contains %d vertices.\n", SIZE);
    breadth_first_search(graph, 0);
    breadth_first_search(graph, 2);
    return 0;
}`,
String.raw`#include <stdio.h>

#define COUNT 8

void print_values(const int values[], int length) {
    for (int index = 0; index < length; ++index) {
        printf("%d", values[index]);
        if (index + 1 < length) {
            printf(" ");
        }
    }
    printf("\n");
}

void insertion_sort(int values[], int length) {
    for (int index = 1; index < length; ++index) {
        int current = values[index];
        int position = index - 1;
        while (position >= 0 && values[position] > current) {
            values[position + 1] = values[position];
            --position;
        }
        values[position + 1] = current;
    }
}

int main(void) {
    int values[COUNT] = { 8, 3, 6, 1, 9, 2, 5, 4 };
    int total = 0;
    printf("Before sorting: ");
    print_values(values, COUNT);
    insertion_sort(values, COUNT);
    printf("After sorting:  ");
    print_values(values, COUNT);

    for (int index = 0; index < COUNT; ++index) {
        total += values[index];
    }
    double mean = (double) total / COUNT;
    printf("Smallest: %d\n", values[0]);
    printf("Largest: %d\n", values[COUNT - 1]);
    printf("Mean: %.2f\n", mean);
    int above_average = 0;
    for (int index = 0; index < COUNT; ++index) {
        if (values[index] > mean) {
            ++above_average;
        }
    }
    printf("Above average: %d\n", above_average);
    printf("Values processed: %d\n", COUNT);
    printf("Sort complete.\n");
    return 0;
}`
  ],
  CPP: [
String.raw`#include <iostream>
#include <queue>
#include <vector>

using Graph = std::vector<std::vector<int>>;

void add_edge(Graph& graph, int first, int second) {
    graph[first].push_back(second);
    graph[second].push_back(first);
}

std::vector<int> breadth_first_search(const Graph& graph, int start) {
    std::vector<bool> visited(graph.size(), false);
    std::queue<int> pending;
    std::vector<int> order;
    visited[start] = true;
    pending.push(start);

    while (!pending.empty()) {
        int current = pending.front();
        pending.pop();
        order.push_back(current);
        for (int neighbour : graph[current]) {
            if (visited[neighbour]) {
                continue;
            }
            visited[neighbour] = true;
            pending.push(neighbour);
        }
    }
    return order;
}

void print_order(const std::vector<int>& order) {
    for (std::size_t index = 0; index < order.size(); ++index) {
        std::cout << order[index];
        if (index + 1 < order.size()) {
            std::cout << " -> ";
        }
    }
    std::cout << '\n';
}

int main() {
    Graph graph(6);
    add_edge(graph, 0, 1);
    add_edge(graph, 0, 2);
    add_edge(graph, 1, 3);
    add_edge(graph, 2, 3);
    add_edge(graph, 3, 4);
    add_edge(graph, 4, 5);
    std::cout << "Traversal from 0: ";
    print_order(breadth_first_search(graph, 0));
    std::cout << "Traversal from 2: ";
    print_order(breadth_first_search(graph, 2));
    return 0;
}`,
String.raw`#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Student {
    std::string name;
    int score;
};

void print_students(const std::vector<Student>& students) {
    for (const Student& student : students) {
        std::cout << student.name << ": " << student.score << '\n';
    }
}

int main() {
    std::vector<Student> students = {
        {"Asha", 82}, {"Dev", 91}, {"Mina", 76},
        {"Ravi", 88}, {"Noor", 95}, {"Ira", 84}
    };
    std::sort(students.begin(), students.end(),
        [](const Student& left, const Student& right) {
            if (left.score != right.score) {
                return left.score > right.score;
            }
            return left.name < right.name;
        });
    std::cout << "Class results\n";
    print_students(students);
    int total = 0;
    for (const Student& student : students) {
        total += student.score;
    }
    double average = static_cast<double>(total) / students.size();
    std::cout << "Average: " << average << '\n';
    if (!students.empty()) {
        std::cout << "Top student: " << students.front().name << '\n';
        std::cout << "Lowest score: " << students.back().score << '\n';
    }
    std::cout << "Students recorded: " << students.size() << '\n';
    int passing = 0;
    for (const Student& student : students) {
        if (student.score >= 80) {
            ++passing;
        }
    }
    std::cout << "Scores at least 80: " << passing << '\n';
    std::cout << "Report complete.\n";
    return 0;
}`
  ],
  JAVA: [
String.raw`import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

public class GraphTraversal {
    private static void addEdge(List<List<Integer>> graph, int a, int b) {
        graph.get(a).add(b);
        graph.get(b).add(a);
    }

    private static List<Integer> breadthFirstSearch(
            List<List<Integer>> graph, int start) {
        boolean[] visited = new boolean[graph.size()];
        Queue<Integer> queue = new ArrayDeque<>();
        List<Integer> order = new ArrayList<>();
        visited[start] = true;
        queue.add(start);

        while (!queue.isEmpty()) {
            int current = queue.remove();
            order.add(current);
            for (int neighbour : graph.get(current)) {
                if (visited[neighbour]) {
                    continue;
                }
                visited[neighbour] = true;
                queue.add(neighbour);
            }
        }
        return order;
    }

    private static List<List<Integer>> createGraph(int size) {
        List<List<Integer>> graph = new ArrayList<>();
        for (int index = 0; index < size; index++) {
            graph.add(new ArrayList<>());
        }
        return graph;
    }

    public static void main(String[] args) {
        List<List<Integer>> graph = createGraph(6);
        addEdge(graph, 0, 1);
        addEdge(graph, 0, 2);
        addEdge(graph, 1, 3);
        addEdge(graph, 2, 3);
        addEdge(graph, 3, 4);
        addEdge(graph, 4, 5);
        System.out.println("From zero: " + breadthFirstSearch(graph, 0));
        System.out.println("From two: " + breadthFirstSearch(graph, 2));
    }
}`,
String.raw`import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class ScoreReport {
    private static class Student {
        private final String name;
        private final int score;

        Student(String name, int score) {
            this.name = name;
            this.score = score;
        }

        @Override
        public String toString() {
            return name + ": " + score;
        }
    }

    public static void main(String[] args) {
        List<Student> students = new ArrayList<>();
        students.add(new Student("Asha", 82));
        students.add(new Student("Dev", 91));
        students.add(new Student("Mina", 76));
        students.add(new Student("Ravi", 88));
        students.add(new Student("Noor", 95));
        students.add(new Student("Ira", 84));
        students.sort(Comparator.comparingInt(
            (Student student) -> student.score).reversed());
        int total = 0;
        System.out.println("Class results");
        for (Student student : students) {
            System.out.println(student);
            total += student.score;
        }
        double average = (double) total / students.size();
        System.out.printf("Average: %.2f%n", average);
        if (!students.isEmpty()) {
            System.out.println("Top student: " + students.get(0).name);
            System.out.println("Lowest score: "
                + students.get(students.size() - 1).score);
        }
        long passing = students.stream().filter(student -> student.score >= 80).count();
        System.out.println("Students recorded: " + students.size());
        System.out.println("Scores at least 80: " + passing);
        System.out.println("Class size: " + students.size());
        System.out.println("Report complete.");
    }
}`
  ],
  PYTHON: [
String.raw`from collections import deque


def add_edge(graph, first, second):
    graph[first].append(second)
    graph[second].append(first)


def breadth_first_search(graph, start):
    visited = {start}
    pending = deque([start])
    order = []
    while pending:
        current = pending.popleft()
        order.append(current)
        for neighbour in graph[current]:
            if neighbour in visited:
                continue
            visited.add(neighbour)
            pending.append(neighbour)
    return order


def build_graph(size):
    return [[] for _ in range(size)]


def print_route(order):
    print(" -> ".join(str(node) for node in order))


def main():
    graph = build_graph(6)
    add_edge(graph, 0, 1)
    add_edge(graph, 0, 2)
    add_edge(graph, 1, 3)
    add_edge(graph, 2, 3)
    add_edge(graph, 3, 4)
    add_edge(graph, 4, 5)
    first_order = breadth_first_search(graph, 0)
    second_order = breadth_first_search(graph, 2)
    print("Traversal from zero:")
    print_route(first_order)
    print("Traversal from two:")
    print_route(second_order)
    print("Visited in first run:", len(first_order))
    print("Visited in second run:", len(second_order))


if __name__ == "__main__":
    main()` ,
String.raw`def merge(left, right):
    result = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1
    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result


def merge_sort(values):
    if len(values) < 2:
        return values[:]
    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    return merge(left, right)


def binary_search(values, target):
    low = 0
    high = len(values) - 1
    while low <= high:
        middle = (low + high) // 2
        if values[middle] == target:
            return middle
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


def main():
    numbers = [19, 4, 12, 7, 2, 15, 9, 1]
    ordered = merge_sort(numbers)
    print("Original:", numbers)
    print("Sorted:", ordered)
    for target in (1, 7, 20):
        print(target, "is at", binary_search(ordered, target))


if __name__ == "__main__":
    main()`
  ],
  WEB: [
String.raw`const tasks = [];
const form = document.querySelector("#task-form");
const input = document.querySelector("#task-name");
const list = document.querySelector("#task-list");
const count = document.querySelector("#task-count");

function createTask(label) {
    return {
        id: crypto.randomUUID(),
        label: label.trim(),
        done: false
    };
}

function addTask(label) {
    if (!label.trim()) {
        return false;
    }
    tasks.push(createTask(label));
    renderTasks();
    return true;
}

function toggleTask(taskId) {
    const task = tasks.find(item => item.id === taskId);
    if (!task) {
        return;
    }
    task.done = !task.done;
    renderTasks();
}

function removeTask(taskId) {
    const index = tasks.findIndex(item => item.id === taskId);
    if (index < 0) {
        return;
    }
    tasks.splice(index, 1);
    renderTasks();
}

function renderTasks() {
    list.replaceChildren();
    for (const task of tasks) {
        const row = document.createElement("li");
        const label = document.createElement("span");
        const toggle = document.createElement("button");
        const remove = document.createElement("button");
        label.textContent = task.label;
        toggle.type = "button";
        toggle.textContent = task.done ? "Undo" : "Complete";
        toggle.setAttribute("aria-pressed", String(task.done));
        remove.type = "button";
        remove.textContent = "Remove";
        toggle.addEventListener("click", () => toggleTask(task.id));
        remove.addEventListener("click", () => removeTask(task.id));
        row.append(label, toggle, remove);
        list.append(row);
    }
    count.textContent = tasks.length + " tasks";
}

form.addEventListener("submit", event => {
    event.preventDefault();
    if (addTask(input.value)) {
        input.value = "";
        input.focus();
    }
});

renderTasks();`,
String.raw`const products = [
    { name: "Notebook", price: 4.5, stock: 12 },
    { name: "Pen set", price: 2.25, stock: 0 },
    { name: "Desk lamp", price: 18.0, stock: 5 },
    { name: "Folder", price: 1.75, stock: 24 },
    { name: "Cable", price: 6.0, stock: 8 }
];

function searchProducts(items, query) {
    const normalized = query.trim().toLowerCase();
    if (!normalized) {
        return items.slice();
    }
    return items.filter(product =>
        product.name.toLowerCase().includes(normalized));
}

function availableProducts(items) {
    return items.filter(product => product.stock > 0);
}

function sortByPrice(items) {
    return items.slice().sort((left, right) =>
        left.price - right.price);
}

function formatProduct(product) {
    const status = product.stock > 0 ? "Available" : "Out of stock";
    return product.name + ": $" + product.price.toFixed(2) + " (" + status + ")";
}

function printProducts(items) {
    if (items.length === 0) {
        console.log("No matching products.");
        return;
    }
    for (const product of items) {
        console.log(formatProduct(product));
    }
}

function totalInventoryValue(items) {
    return items.reduce((total, product) =>
        total + product.price * product.stock, 0);
}

function main() {
    console.log("All products:");
    printProducts(products);
    console.log("Available products by price:");
    printProducts(sortByPrice(availableProducts(products)));
    console.log("Search for desk:");
    printProducts(searchProducts(products, "desk"));
    console.log("Inventory value:",
        totalInventoryValue(products).toFixed(2));
}

main();`
  ]
};

/* A third full-program variant changes the graph or sample data per language. */
STUDY_TYPING_PROGRAMS.C.push(STUDY_TYPING_PROGRAMS.C[0]
    .replace('#define SIZE 6', '#define SIZE 7')
    .replace('    add_edge(graph, 4, 5);', '    add_edge(graph, 4, 5);\n    add_edge(graph, 5, 6);'));
STUDY_TYPING_PROGRAMS.CPP.push(STUDY_TYPING_PROGRAMS.CPP[0]
    .replace('Graph graph(6);', 'Graph graph(7);')
    .replace('add_edge(graph, 4, 5);', 'add_edge(graph, 4, 5);\n    add_edge(graph, 5, 6);'));
STUDY_TYPING_PROGRAMS.JAVA.push(STUDY_TYPING_PROGRAMS.JAVA[0]
    .replace('createGraph(6);', 'createGraph(7);')
    .replace('addEdge(graph, 4, 5);', 'addEdge(graph, 4, 5);\n        addEdge(graph, 5, 6);'));
STUDY_TYPING_PROGRAMS.PYTHON.push(STUDY_TYPING_PROGRAMS.PYTHON[0]
    .replace('build_graph(6)', 'build_graph(7)')
    .replace('    add_edge(graph, 4, 5)', '    add_edge(graph, 4, 5)\n    add_edge(graph, 5, 6)'));
STUDY_TYPING_PROGRAMS.WEB.push(STUDY_TYPING_PROGRAMS.WEB[1]
    .replace('"Notebook", price: 4.5, stock: 12', '"Planner", price: 7.5, stock: 9')
    .replace('"Pen set", price: 2.25, stock: 0', '"Marker set", price: 3.25, stock: 4')
    .replace('"Desk lamp", price: 18.0, stock: 5', '"Reading light", price: 15.0, stock: 7'));
STUDY_TYPING_PROGRAMS.C.push(STUDY_TYPING_PROGRAMS.C[1]
    .replace('{ 8, 3, 6, 1, 9, 2, 5, 4 }', '{ 14, 7, 3, 11, 6, 2, 10, 5 }'));
STUDY_TYPING_PROGRAMS.CPP.push(STUDY_TYPING_PROGRAMS.CPP[1]
    .replace('{"Asha", 82}', '{"Asha", 89}')
    .replace('{"Dev", 91}', '{"Dev", 73}')
    .replace('{"Mina", 76}', '{"Mina", 94}'));
STUDY_TYPING_PROGRAMS.JAVA.push(STUDY_TYPING_PROGRAMS.JAVA[1]
    .replace('("Asha", 82)', '("Asha", 89)')
    .replace('("Dev", 91)', '("Dev", 73)')
    .replace('("Mina", 76)', '("Mina", 94)'));
STUDY_TYPING_PROGRAMS.PYTHON.push(STUDY_TYPING_PROGRAMS.PYTHON[1]
    .replace('[19, 4, 12, 7, 2, 15, 9, 1]', '[21, 8, 3, 17, 6, 14, 2, 11]'));
STUDY_TYPING_PROGRAMS.WEB.push(STUDY_TYPING_PROGRAMS.WEB[1]
    .replace('"Notebook", price: 4.5, stock: 12', '"Sketchbook", price: 6.5, stock: 16')
    .replace('"Pen set", price: 2.25, stock: 0', '"Ink set", price: 8.25, stock: 3')
    .replace('"Desk lamp", price: 18.0, stock: 5', '"Book stand", price: 11.0, stock: 2'));

if (typeof window !== 'undefined') window.STUDY_TYPING_PROGRAMS = STUDY_TYPING_PROGRAMS;
if (typeof module !== 'undefined' && module.exports) module.exports = STUDY_TYPING_PROGRAMS;
