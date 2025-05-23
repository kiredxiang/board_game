'''
游戏管理类 (BoardGameManager)
功能：作为游戏的核心控制器，负责管理游戏状态、协调各组件交互。
'''

class BoardGameManager:
    _instance = None

    @staticmethod
    def get_instance():
        """获取单例实例"""
        if BoardGameManager._instance is None:
            BoardGameManager._instance = BoardGameManager()
        return BoardGameManager._instance

    def __init__(self):
        if BoardGameManager._instance is not None:
            raise Exception("单例类不能直接实例化，请使用get_instance方法")

        self.current_game = None
        self.observers = []

    def start_new_game(self, game):
        """开始新游戏"""
        self.current_game = game
        self.notify_observers()

    # game_logic/game_manager.py

    def make_move(self, x, y):
        """处理落子请求"""
        if self.current_game and self.current_game.make_move(x, y):
            # 打印调试信息
            print(f"落子成功: ({x}, {y}), 当前玩家: {self.current_game.current_player}")

            # 检查是否获胜
            if self.current_game.check_win(x, y):
                print(f"游戏结束，玩家{self.current_game.winner}获胜！")

            self.notify_observers()
            return True
        print(f"落子失败: ({x}, {y})")
        return False

    def undo_move(self):
        """处理悔棋请求"""
        if self.current_game and self.current_game.undo_move():
            self.notify_observers()
            return True
        return False

    def add_observer(self, observer):
        """添加观察者"""
        self.observers.append(observer)

    def remove_observer(self, observer):
        """移除观察者"""
        self.observers.remove(observer)

    def notify_observers(self):
        """通知所有观察者游戏状态已更新"""
        for observer in self.observers:
            observer()