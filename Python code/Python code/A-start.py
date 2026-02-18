import tkinter as tk
from tkinter import messagebox
import math

# 定义全局变量
CELL_SIZE = 60  # 每个网格单元的大小
GRID_WIDTH = 10  # 网格宽度
GRID_HEIGHT = 10  # 网格高度


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')  # 从起点到当前节点的成本
        self.h = 0  # 从当前节点到终点的估算成本
        self.f = float('inf')  # 总成本 (g + h)
        self.parent = None
        self.is_obstacle = False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class AStarVisualization:
    def __init__(self, root):
        self.root = root
        self.root.title("A*算法路径规划演示")

        # 创建网格
        self.grid = [[Node(x, y) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]

        # 设置起点和终点
        self.start_node = self.grid[1][1]
        self.end_node = self.grid[8][8]

        # 设置障碍物
        self.set_obstacles()

        # 初始化算法状态
        self.open_list = []
        self.closed_list = []
        self.current_step = 0
        self.is_completed = False
        self.path = []

        # 创建画布
        self.canvas = tk.Canvas(root, width=GRID_WIDTH * CELL_SIZE, height=GRID_HEIGHT * CELL_SIZE, bg="white")
        self.canvas.pack(pady=10)

        # 创建控制按钮
        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)

        self.step_button = tk.Button(control_frame, text="下一步", command=self.next_step)
        self.step_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(control_frame, text="重置", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # 信息显示
        self.info_label = tk.Label(root, text="点击'下一步'开始A*算法演示", font=("Arial", 12))
        self.info_label.pack(pady=5)

        # 绘制初始网格
        self.draw_grid()

        # 初始化算法
        self.initialize_algorithm()

    def set_obstacles(self):
        # 设置一些障碍物
        obstacles = [
            (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
            (5, 4), (5, 5), (5, 6), (5, 7),
            (7, 1), (7, 2), (7, 3)
        ]

        for x, y in obstacles:
            self.grid[x][y].is_obstacle = True

    def initialize_algorithm(self):
        # 重置算法状态
        self.open_list = []
        self.closed_list = []
        self.current_step = 0
        self.is_completed = False
        self.path = []

        # 重置所有节点
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                self.grid[x][y].g = float('inf')
                self.grid[x][y].f = float('inf')
                self.grid[x][y].parent = None

        # 初始化起点
        self.start_node.g = 0
        self.start_node.h = self.heuristic(self.start_node, self.end_node)
        self.start_node.f = self.start_node.g + self.start_node.h
        self.open_list.append(self.start_node)

        self.info_label.config(text="算法已初始化，点击'下一步'开始")

    def heuristic(self, node1, node2):
        # 使用曼哈顿距离作为启发式函数
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)

    def get_neighbors(self, node):
        neighbors = []
        # 定义四个方向的偏移量（右、下、左、上）
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for dx, dy in directions:
            x, y = node.x + dx, node.y + dy
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and not self.grid[x][y].is_obstacle:
                neighbors.append(self.grid[x][y])

        return neighbors

    def next_step(self):
        if self.is_completed:
            messagebox.showinfo("完成", "路径规划已完成！")
            return

        self.current_step += 1

        if not self.open_list:
            messagebox.showinfo("无解", "找不到从起点到终点的路径！")
            self.is_completed = True
            return

        # 找到f值最小的节点
        current_node = min(self.open_list, key=lambda node: node.f)

        # 如果到达终点
        if current_node == self.end_node:
            self.reconstruct_path(current_node)
            self.is_completed = True
            self.info_label.config(text=f"步骤 {self.current_step}: 找到路径！")
            self.draw_grid()
            return

        # 将当前节点从开放列表移到关闭列表
        self.open_list.remove(current_node)
        self.closed_list.append(current_node)

        # 获取邻居节点
        neighbors = self.get_neighbors(current_node)

        for neighbor in neighbors:
            if neighbor in self.closed_list:
                continue

            # 计算从起点经过当前节点到邻居节点的成本
            tentative_g = current_node.g + 1  # 假设每个移动的成本为1

            if neighbor not in self.open_list:
                self.open_list.append(neighbor)
            elif tentative_g >= neighbor.g:
                continue

            # 这条路径更好，记录它
            neighbor.parent = current_node
            neighbor.g = tentative_g
            neighbor.h = self.heuristic(neighbor, self.end_node)
            neighbor.f = neighbor.g + neighbor.h

        # 更新显示
        self.info_label.config(
            text=f"步骤 {self.current_step}: 当前节点 ({current_node.x}, {current_node.y}), f值: {current_node.f}")
        self.draw_grid()

    def reconstruct_path(self, node):
        # 从终点回溯到起点，重建路径
        current = node
        while current is not None:
            self.path.append(current)
            current = current.parent
        self.path.reverse()

    def reset(self):
        # 重置所有障碍物状态
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                self.grid[x][y].is_obstacle = False

        # 重新设置障碍物
        self.set_obstacles()

        # 重新初始化算法
        self.initialize_algorithm()

        # 重绘画布
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")

        # 绘制网格线
        for i in range(GRID_WIDTH + 1):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, GRID_HEIGHT * CELL_SIZE, fill="gray")
        for i in range(GRID_HEIGHT + 1):
            self.canvas.create_line(0, i * CELL_SIZE, GRID_WIDTH * CELL_SIZE, i * CELL_SIZE, fill="gray")

        # 绘制节点
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                node = self.grid[x][y]
                x1 = x * CELL_SIZE
                y1 = y * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                # 设置节点颜色
                if node == self.start_node:
                    color = "blue"
                elif node == self.end_node:
                    color = "red"
                elif node.is_obstacle:
                    color = "black"
                elif node in self.path:
                    color = "purple"
                elif node in self.closed_list:
                    color = "lightblue"
                elif node in self.open_list