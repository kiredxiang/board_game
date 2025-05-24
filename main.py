import tkinter as tk
from game_logic.game_manager import BoardGameManager
from game_logic.game_gomoku import GomokuGame
from ui.main_window import MainWindow
from game_logic.game_manager import BoardGameManager  # 添加这行导入BoardGameManager类


if __name__ == "__main__":
    # 初始化游戏管理
    game_manager = BoardGameManager.get_instance()
    game_manager.start_new_game(GomokuGame(board_size=15))

    # 创建并运行主窗口
    root = MainWindow()
    root.mainloop()