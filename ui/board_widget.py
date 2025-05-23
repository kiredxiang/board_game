'''
棋盘组件类 (BoardWidget)
功能：继承自tkinter.Canvas，实现棋盘的绘制和交互功能。
'''
import tkinter as tk


class BoardWidget(tk.Canvas):
    def __init__(self, master, click_callback=None, board_size=15, cell_size=40):
        super().__init__(master, bg="#E6C38D", highlightthickness=0)
        self.board_size = board_size
        self.cell_size = cell_size
        self.click_callback = click_callback
        self.stones = {}  # 存储棋子的ID

        # 计算画布大小（增加边距）
        self.margin = 40  # 边距
        self.canvas_width = self.board_size * self.cell_size + 2 * self.margin
        self.canvas_height = self.board_size * self.cell_size + 2 * self.margin

        # 设置画布尺寸
        self.config(width=self.canvas_width, height=self.canvas_height)

        # 绑定鼠标点击事件
        self.bind("<Button-1>", self.on_click)

        # 初始绘制棋盘
        self.draw_grid()

    def set_board_size(self, size):
        """设置棋盘大小"""
        self.board_size = size
        self.canvas_width = self.board_size * self.cell_size + 2 * self.margin
        self.canvas_height = self.board_size * self.cell_size + 2 * self.margin
        self.config(width=self.canvas_width, height=self.canvas_height)
        self.clear_board()
        self.draw_grid()

    def draw_grid(self):
        """绘制棋盘网格"""
        self.delete("grid")  # 清除现有网格

        # 绘制横线和竖线
        for i in range(self.board_size):
            # 计算坐标（添加边距）
            y = self.margin + i * self.cell_size

            # 横线
            self.create_line(
                self.margin, y,
                self.canvas_width - self.margin, y,
                width=1, tags="grid"
            )

            # 竖线
            x = self.margin + i * self.cell_size
            self.create_line(
                x, self.margin,
                x, self.canvas_height - self.margin,
                width=1, tags="grid"
            )

        # 绘制边缘线（加粗）
        self.create_line(
            self.margin, self.margin,
            self.canvas_width - self.margin, self.margin,
            width=2, tags="grid"
        )
        self.create_line(
            self.margin, self.canvas_height - self.margin,
                         self.canvas_width - self.margin, self.canvas_height - self.margin,
            width=2, tags="grid"
        )
        self.create_line(
            self.margin, self.margin,
            self.margin, self.canvas_height - self.margin,
            width=2, tags="grid"
        )
        self.create_line(
            self.canvas_width - self.margin, self.margin,
            self.canvas_width - self.margin, self.canvas_height - self.margin,
            width=2, tags="grid"
        )

        # 绘制天元和星位（五子棋通常在15x15棋盘上有这些标记）
        if self.board_size == 15:
            star_points = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
            for x, y in star_points:
                cx = self.margin + x * self.cell_size
                cy = self.margin + y * self.cell_size
                self.create_oval(
                    cx - 3, cy - 3,
                    cx + 3, cy + 3,
                    fill="black", tags="grid"
                )

    def draw_stone(self, x, y, player):
        """绘制棋子"""
        print(
            f"绘制棋子: 棋盘坐标({x}, {y}), 像素坐标({self.margin + x * self.cell_size}, {self.margin + y * self.cell_size})")

        # 计算像素坐标（添加边距）
        px = self.margin + x * self.cell_size
        py = self.margin + y * self.cell_size

        # 棋子颜色
        color = "black" if player == 1 else "white"

        # 创建棋子
        stone_id = self.create_oval(
            px - 20, py - 20,
            px + 20, py + 20,
            fill=color, outline="black", width=1,
            tags=f"stone_{x}_{y}"
        )

        # 确保棋子显示在最上层
        self.tag_raise(stone_id)

        # 添加到棋子字典
        self.stones[(x, y)] = stone_id

        # 添加动画效果
        # self.animate_stone(stone_id, 0, 1)

    def animate_stone(self, stone_id, start_size, end_size):
        """棋子落下动画"""
        current_size = start_size
        steps = 10

        def update_size():
            nonlocal current_size
            if current_size < end_size:
                current_size += 1 / steps
                scale = current_size
                self.scale(stone_id, 0, 0, scale, scale)
                self.after(10, update_size)

        update_size()

    def clear_board(self):
        """清除棋盘上的所有棋子"""
        all_objects = self.find_all()
        for obj in all_objects:
            tags = self.gettags(obj)
            for tag in tags:
                if "stone" in tag:
                    self.delete(obj)
                    break
        self.stones = {}

    def refresh_board(self, board_data):
        """根据棋盘数据刷新显示"""
        self.clear_board()
        for x in range(self.board_size):
            for y in range(self.board_size):
                if board_data[x][y] != 0:
                    self.draw_stone(x, y, board_data[x][y])

    def on_click(self, event):
        """处理鼠标点击事件"""
        # 计算点击的棋盘坐标（考虑边距）
        x = round((event.x - self.margin) / self.cell_size)
        y = round((event.y - self.margin) / self.cell_size)

        # 检查坐标是否在有效范围内
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            # 调用回调函数
            if self.click_callback:
                print(f"棋盘点击: 像素坐标({event.x}, {event.y}), 棋盘坐标({x}, {y})")
                self.click_callback(x, y)