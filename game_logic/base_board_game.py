'''
游戏基类
功能：定义所有棋类游戏的通用接口和基础逻辑
'''
class BaseBoardGame:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]  # 0:空, 1:黑, 2:白
        self.current_player = 1  # 1:黑棋先手
        self.move_history = []  # 记录落子历史，用于悔棋
        self.game_over = False
        self.winner = 0  # 0:未结束, 1:黑胜, 2:白胜

    def is_valid_move(self, x, y):
        """检查落子是否合法"""
        # 检查坐标是否在范围内
        if x < 0 or x >= self.board_size or y < 0 or y >= self.board_size:
            print(f"无效坐标: ({x}, {y})")
            return False

        # 检查位置是否为空
        if self.board[x][y] != 0:
            print(f"位置已被占用: ({x}, {y})，当前值: {self.board[x][y]}")
            return False

        return True

    def make_move(self, x, y):
        """落子并更新游戏状态"""
        if not self.is_valid_move(x, y):
            return False

        self.board[x][y] = self.current_player
        self.move_history.append((x, y, self.current_player))
        self.current_player = 3 - self.current_player  # 切换玩家(1<->2)
        return True

    def undo_move(self):
        """悔棋操作"""
        if not self.move_history:
            return False

        x, y, player = self.move_history.pop()
        self.board[x][y] = 0
        self.current_player = player  # 恢复当前玩家
        self.game_over = False
        self.winner = 0
        return True

    def check_win(self, x, y):
        """检查是否获胜，由子类实现"""
        raise NotImplementedError

    def get_status(self):
        """获取当前游戏状态"""
        return {
            'board': self.board,
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner,
            'board_size': self.board_size
        }

    def reset(self):
        """重置游戏"""
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 1
        self.move_history = []
        self.game_over = False
        self.winner = 0