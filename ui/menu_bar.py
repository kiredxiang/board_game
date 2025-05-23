'''
菜单栏类 (MenuBar)
功能：创建并管理菜单栏，提供游戏的基本操作选项。
'''
import tkinter as tk
from tkinter import filedialog, messagebox


class MenuBar(tk.Menu):
    def __init__(self, master, main_window):
        super().__init__(master)
        self.main_window = main_window
        self.game_manager = main_window.game_manager
        self.save_load_manager = main_window.save_load_manager

        # 创建文件菜单
        self.file_menu = tk.Menu(self, tearoff=0)
        self.file_menu.add_command(label="新游戏", command=self.main_window.start_new_game, accelerator="Ctrl+N")
        self.file_menu.add_command(label="保存游戏", command=self.save_game, accelerator="Ctrl+S")
        self.file_menu.add_command(label="加载游戏", command=self.load_game, accelerator="Ctrl+L")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="退出", command=self.master.quit, accelerator="Ctrl+Q")
        self.add_cascade(label="文件", menu=self.file_menu)

        # 创建游戏菜单
        self.game_menu = tk.Menu(self, tearoff=0)
        self.game_menu.add_command(label="悔棋", command=self.main_window.on_undo_click, accelerator="Ctrl+Z")
        self.game_menu.add_command(label="重新开始", command=self.main_window.start_new_game, accelerator="Ctrl+R")
        self.game_menu.add_separator()
        self.game_menu.add_command(label="关于", command=self.show_about)
        self.add_cascade(label="游戏", menu=self.game_menu)

        # 绑定快捷键
        self.master.bind("<Control-n>", lambda event: self.main_window.start_new_game())
        self.master.bind("<Control-s>", lambda event: self.save_game())
        self.master.bind("<Control-l>", lambda event: self.load_game())
        self.master.bind("<Control-q>", lambda event: self.master.quit())
        self.master.bind("<Control-z>", lambda event: self.main_window.on_undo_click())
        self.master.bind("<Control-r>", lambda event: self.main_window.start_new_game())

    def save_game(self):
        """保存游戏"""
        if not self.game_manager.current_game:
            messagebox.showinfo("提示", "没有正在进行的游戏")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="保存游戏"
        )

        if file_path:
            try:
                self.save_load_manager.save_game(self.game_manager.current_game, file_path)
                messagebox.showinfo("成功", f"游戏已保存到 {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存游戏失败: {str(e)}")

    def load_game(self):
        """加载游戏"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="加载游戏"
        )

        if file_path:
            try:
                game = self.save_load_manager.load_game(file_path)
                if game:
                    self.game_manager.start_new_game(game)
                    self.main_window.board_widget.set_board_size(game.board_size)
                    self.main_window.board_widget.refresh_board(game.board)
                    self.main_window.clear_history()

                    # 恢复历史记录
                    for i, (x, y, player) in enumerate(game.move_history):
                        player_text = "黑棋" if player == 1 else "白棋"
                        self.main_window.update_history(f"第{i + 1}步: {player_text} ({x}, {y})")

                    messagebox.showinfo("成功", f"游戏已从 {file_path} 加载")
            except Exception as e:
                messagebox.showerror("错误", f"加载游戏失败: {str(e)}")

    def show_about(self):
        """显示关于对话框"""
        about_text = "五子棋对战平台\n\n" \
                     "版本: 1.0\n" \
                     "作者: 向全洪\n" \
                     "描述: 一个基于Python和tkinter的五子棋和围棋的对战游戏\n" \
                     "功能: 双人对战、悔棋、保存/加载游戏"

        messagebox.showinfo("关于", about_text)