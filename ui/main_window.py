'''
主窗口类 (MainWindow)
功能：初始化时创建 BoardGameManager 和 BoardWidget。
'''

import tkinter as tk
from tkinter import messagebox, simpledialog
from ui.board_widget import BoardWidget
from ui.menu_bar import MenuBar
from utils.save_load import SaveLoadManager
from game_logic.game_manager import BoardGameManager
from game_logic.board_game_factory import BoardGameFactory


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("棋类对战平台")
        self.geometry("800x600")
        self.resizable(True, True)

        # 初始化保存加载管理器
        self.save_load_manager = SaveLoadManager()

        # 游戏类型和棋盘大小
        self.game_type = "gomoku"  # 默认五子棋
        self.board_size = 15  # 默认棋盘大小

        # 创建并配置主框架
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建左侧棋盘区域
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建右侧信息和控制区域
        self.info_frame = tk.Frame(self.main_frame, width=200, bg="#f0f0f0")
        self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        self.info_frame.pack_propagate(False)

        # 初始化游戏管理器并添加观察者
        self.game_manager = BoardGameManager.get_instance()
        self.game_manager.add_observer(self.update_ui)

        # 创建棋盘组件
        self.board_widget = BoardWidget(self.board_frame, self.on_board_click)
        self.board_widget.pack(fill=tk.BOTH, expand=True)

        # 创建菜单
        self.menu_bar = MenuBar(self, self)
        self.config(menu=self.menu_bar)

        # 创建游戏信息显示
        self.create_game_info_panel()

        # 初始化新游戏
        self.start_new_game()


    def create_game_info_panel(self):
        """创建游戏信息面板"""
        # 游戏类型标签
        self.game_type_label = tk.Label(self.info_frame, text="游戏类型: 五子棋", font=("SimHei", 14), bg="#f0f0f0")
        self.game_type_label.pack(pady=10)

        # 棋盘大小标签
        self.size_label = tk.Label(self.info_frame, text="棋盘大小: 15×15", font=("SimHei", 14), bg="#f0f0f0")
        self.size_label.pack(pady=10)

        # 游戏状态标签
        self.status_label = tk.Label(self.info_frame, text="游戏状态: 进行中", font=("SimHei", 14), bg="#f0f0f0")
        self.status_label.pack(pady=10)

        # 当前玩家标签
        self.player_label = tk.Label(self.info_frame, text="当前玩家: 黑棋", font=("SimHei", 14), bg="#f0f0f0")
        self.player_label.pack(pady=10)

        # 操作按钮
        self.button_frame = tk.Frame(self.info_frame, bg="#f0f0f0")
        self.button_frame.pack(fill=tk.X, padx=20, pady=20)

        self.undo_button = tk.Button(self.button_frame, text="悔棋", command=self.on_undo_click,
                                     font=("SimHei", 12), bg="#e0e0e0", relief=tk.RAISED)
        self.undo_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.reset_button = tk.Button(self.button_frame, text="重新开始", command=self.start_new_game,
                                      font=("SimHei", 12), bg="#e0e0e0", relief=tk.RAISED)
        self.reset_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)

        # 围棋特有的Pass按钮
        self.pass_button = tk.Button(self.info_frame, text="Pass", command=self.on_pass_click,
                                     font=("SimHei", 12), bg="#e0e0e0", relief=tk.RAISED, state=tk.NORMAL)
        self.pass_button.pack(fill=tk.X, padx=20, pady=5)

        # 历史记录区域
        self.history_frame = tk.Frame(self.info_frame, bg="#f0f0f0")
        self.history_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.history_label = tk.Label(self.history_frame, text="历史记录", font=("SimHei", 12), bg="#f0f0f0")
        self.history_label.pack(anchor=tk.W)

        self.history_text = tk.Text(self.history_frame, height=10, width=20, font=("SimHei", 10),
                                    bg="#ffffff", relief=tk.SUNKEN)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        self.history_text.config(state=tk.DISABLED)

        # 退出按钮
        self.exit_button = tk.Button(self.info_frame, text="退出游戏", command=self.on_exit_click,
                                     font=("SimHei", 12), bg="#e0e0e0", relief=tk.RAISED)
        self.exit_button.pack(fill=tk.X, padx=20, pady=5)

        # 认输按钮
        self.surrender_button = tk.Button(self.info_frame, text="认输", command=self.on_surrender_click,
                                          font=("SimHei", 12), bg="#e0e0e0", relief=tk.RAISED)
        self.surrender_button.pack(fill=tk.X, padx=20, pady=5)

    def on_exit_click(self):
        """处理退出按钮点击"""
        if messagebox.askyesno("确认退出", "确定要退出游戏吗？"):
            self.quit()  # 退出主循环
            self.destroy()  # 销毁窗口
    def start_new_game(self):
        """开始新游戏"""
        # 选择游戏类型
        game_type = self.select_game_type()
        if game_type is None:
            return  # 用户取消

        self.game_type = game_type

        # 获取棋盘大小（根据游戏类型设置默认值）
        default_size = 15 if game_type == "gomoku" else 19
        min_size = 8
        max_size = 19

        while True:
            size = simpledialog.askinteger(
                "棋盘大小",
                f"请输入棋盘大小 ({min_size}-{max_size}, 默认{default_size}):",
                minvalue=min_size,
                maxvalue=max_size,
                parent=self
            )

            if size is None:  # 用户取消
                return

            if min_size <= size <= max_size:
                break
            else:
                messagebox.showerror("输入错误", f"请输入{min_size}到{max_size}之间的数字")

        self.board_size = size

        # 创建新游戏
        game = BoardGameFactory.create_game(game_type, size)
        self.game_manager.start_new_game(game)

        # 更新游戏类型和棋盘大小标签
        game_name = "五子棋" if game_type == "gomoku" else "围棋"
        self.game_type_label.config(text=f"游戏类型: {game_name}")
        self.size_label.config(text=f"棋盘大小: {size}×{size}")

        # 启用/禁用Pass按钮
        self.pass_button.config(state=tk.NORMAL if game_type == "go" else tk.DISABLED)

        # 重置棋盘显示
        self.board_widget.set_board_size(size)
        self.board_widget.clear_board()

        # 清空历史记录
        self.clear_history()

        # 更新UI
        self.update_ui()

    def on_surrender_click(self):
        """处理认输按钮点击"""
        current_player = self.game_manager.current_game.current_player
        player_text = "黑棋" if current_player == 1 else "白棋"

        if messagebox.askyesno("确认认输", f"确定要认输吗？\n{player_text}将输掉此局。"):
            # 设置游戏结束并指定胜利者
            self.game_manager.current_game.game_over = True
            self.game_manager.current_game.winner = 3 - current_player  # 对手获胜

            # 更新UI
            self.update_ui()

            # 显示结果
            winner_text = "黑棋" if self.game_manager.current_game.winner == 1 else "白棋"
            messagebox.showinfo("游戏结束", f"{winner_text}获胜！")

            # 记录到历史
            self.update_history(f"{player_text}认输，{winner_text}获胜")

    def select_game_type(self):
        """选择游戏类型对话框"""
        game_window = tk.Toplevel(self)
        game_window.title("选择游戏类型")
        game_window.geometry("300x200")
        game_window.transient(self)
        game_window.grab_set()

        result = None

        def on_gomoku_selected():
            nonlocal result
            result = "gomoku"
            game_window.destroy()

        def on_go_selected():
            nonlocal result
            result = "go"
            game_window.destroy()

        tk.Label(game_window, text="请选择游戏类型:", font=("SimHei", 14)).pack(pady=20)

        tk.Button(game_window, text="五子棋", command=on_gomoku_selected,
                  font=("SimHei", 12), width=15).pack(pady=10)

        tk.Button(game_window, text="围棋", command=on_go_selected,
                  font=("SimHei", 12), width=15).pack(pady=10)

        self.wait_window(game_window)
        return result

    def on_board_click(self, x, y):
        """处理棋盘点击事件"""
        if self.game_type == "go" and self.game_manager.current_game.game_over:
            return

        print(f"尝试落子: ({x}, {y}), 当前玩家: {self.game_manager.current_game.current_player}")

        if self.game_manager.make_move(x, y):
            # 落子成功，手动绘制棋子
            player = self.game_manager.current_game.board[x][y]
            self.board_widget.draw_stone(x, y, player)

            # 落子成功，更新历史记录
            player_text = "黑棋" if player == 1 else "白棋"
            self.update_history(f"{player_text} ({x}, {y})")

            # 检查游戏是否结束
            if self.game_manager.current_game.game_over:
                if self.game_type == "gomoku":
                    winner = "黑棋" if self.game_manager.current_game.winner == 1 else "白棋"
                    messagebox.showinfo("游戏结束", f"{winner}获胜！")
                    self.status_label.config(text=f"游戏状态: {winner}获胜")
                else:  # 围棋
                    winner = "黑棋" if self.game_manager.current_game.winner == 1 else "白棋"
                    messagebox.showinfo("游戏结束", f"{winner}获胜！")
                    self.status_label.config(text=f"游戏状态: {winner}获胜")

    def on_undo_click(self):
        """处理悔棋按钮点击"""
        if self.game_manager.undo_move():
            # 刷新棋盘
            self.board_widget.refresh_board(self.game_manager.current_game.board)

            # 更新状态
            if self.game_manager.current_game.game_over:
                self.status_label.config(text="游戏状态: 进行中")

    def on_pass_click(self):
        """处理Pass按钮点击（围棋）"""
        if self.game_type == "go":
            if self.game_manager.current_game.pass_move():
                player_text = "黑棋" if self.game_manager.current_game.current_player == 2 else "白棋"
                self.update_history(f"{player_text} Pass")

                # 检查游戏是否结束
                if self.game_manager.current_game.game_over:
                    winner = "黑棋" if self.game_manager.current_game.winner == 1 else "白棋"
                    messagebox.showinfo("游戏结束", f"{winner}获胜！")
                    self.status_label.config(text=f"游戏状态: {winner}获胜")

    def update_ui(self):
        """更新UI显示"""
        game_state = self.game_manager.current_game.get_status()

        # 更新当前玩家标签
        player_text = "黑棋" if game_state['current_player'] == 1 else "白棋"
        self.player_label.config(text=f"当前玩家: {player_text}")

        # 更新状态标签
        if game_state['game_over']:
            if self.game_type == "gomoku":
                winner_text = "黑棋" if game_state['winner'] == 1 else "白棋"
                self.status_label.config(text=f"游戏状态: {winner_text}获胜")
            else:  # 围棋
                winner_text = "黑棋" if game_state['winner'] == 1 else "白棋"
                self.status_label.config(text=f"游戏状态: {winner_text}获胜")
        else:
            self.status_label.config(text="游戏状态: 进行中")

    def update_history(self, text):
        """更新历史记录"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, text + "\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)

    def clear_history(self):
        """清空历史记录"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)

    def on_pass_click(self):
        if self.game_manager.pass_move():
            player_text = "黑棋" if self.game_manager.current_game.current_player == 2 else "白棋"
            self.update_history(f"{player_text} Pass")
            self.update_ui()
            # 检查是否达到连续Pass结束条件
            pass_count = self.game_manager.current_game.move_history.count((-1, -1, 1)) + self.game_manager.current_game.move_history.count((-1, -1, 2))
            if pass_count >= 2:
                self.game_manager.current_game.game_over = True
                self.game_manager.current_game._determine_winner()  # 需完善此方法判断五子棋胜负
                self.update_ui()
                winner = "黑棋" if self.game_manager.current_game.winner == 1 else "白棋"
                messagebox.showinfo("游戏结束", f"{winner}获胜！")