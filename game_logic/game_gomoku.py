'''
五子棋类
功能：继承自BaseBoardGame，实现五子棋的特定规则。
'''
from .base_board_game import BaseBoardGame
class GomokuGame(BaseBoardGame):
    def __init__(self, board_size=15):
        super().__init__(board_size)

    def check_win(self, x, y):
        """检查是否连成五子"""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 水平、垂直、对角线、反对角线
        player = self.board[x][y]

        for dx, dy in directions:
            count = 1  # 当前位置已经有一个棋子

            # 检查正方向
            i, j = x + dx, y + dy
            while (0 <= i < self.board_size and
                   0 <= j < self.board_size and
                   self.board[i][j] == player):
                count += 1
                i += dx
                j += dy

            # 检查反方向
            i, j = x - dx, y - dy
            while (0 <= i < self.board_size and
                   0 <= j < self.board_size and
                   self.board[i][j] == player):
                count += 1
                i -= dx
                j -= dy

            if count >= 5:
                self.game_over = True
                self.winner = player
                return True

        return False