'''
围棋类
功能：继承自BaseBoardGame，实现围棋的复杂规则。

'''
from game_logic.base_board_game import BaseBoardGame
class GoGame(BaseBoardGame):
    def __init__(self, board_size=19):
        super().__init__(board_size)
        self.liberty_board = [[0 for _ in range(board_size)] for _ in range(board_size)]  # 记录每格的气
        self.history_boards = []  # 记录历史棋盘状态，用于判断劫
        self.current_player = 1  # 1:黑棋先手
        self.pass_count = 0  # 记录连续pass次数，用于判断游戏结束
        self.komi = 6.5  # 贴目

    def is_valid_move(self, x, y):
        """检查落子是否合法（围棋规则）"""
        if not super().is_valid_move(x, y):
            return False

        # 检查是否是自杀行为（没有气且不能提子）
        temp_board = [row.copy() for row in self.board]
        temp_board[x][y] = self.current_player

        # 计算自身气数
        if self._calculate_liberty(temp_board, x, y, self.current_player) <= 0:
            # 检查是否能提掉对方的棋子
            opponent = 3 - self.current_player
            captured = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if temp_board[nx][ny] == opponent and self._calculate_liberty(temp_board, nx, ny, opponent) <= 0:
                        captured = True
                        break
            if not captured:
                return False  # 自杀行为，无效

        # 检查劫争（禁止立即回提）
        if self._is_ko(temp_board, x, y):
            return False

        return True

    def make_move(self, x, y):
        """落子并更新游戏状态（围棋规则）"""
        if not self.is_valid_move(x, y):
            return False

        # 记录历史状态
        self.history_boards.append([row.copy() for row in self.board])

        # 落子
        self.board[x][y] = self.current_player
        self.move_history.append((x, y, self.current_player))

        # 提子
        opponent = 3 - self.current_player
        captured_stones = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if self.board[nx][ny] == opponent and self._calculate_liberty(self.board, nx, ny, opponent) <= 0:
                    # 该组棋子没有气，提子
                    self._remove_stones(nx, ny, opponent, captured_stones)

        # 更新气数棋盘
        self._update_liberty_board()

        # 检查是否形成眼
        if self._is_eye(x, y, self.current_player):
            print(f"玩家{self.current_player}在({x}, {y})形成眼")

        # 切换玩家
        self.current_player = opponent
        self.pass_count = 0  # 落子后重置pass计数
        return True

    def pass_move(self):
        """玩家放弃回合（Pass）"""
        self.history_boards.append([row.copy() for row in self.board])
        self.move_history.append((-1, -1, self.current_player))  # -1表示pass
        self.current_player = 3 - self.current_player
        self.pass_count += 1

        # 连续两次pass，游戏结束
        if self.pass_count >= 2:
            self.game_over = True
            self._determine_winner()

        return True

    def _calculate_liberty(self, board, x, y, player):
        """计算一组棋子的气数"""
        if board[x][y] != player:
            return 0

        visited = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
        queue = [(x, y)]
        visited[x][y] = True
        liberty = 0

        while queue:
            cx, cy = queue.pop(0)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if board[nx][ny] == 0 and not visited[nx][ny]:
                        liberty += 1
                        visited[nx][ny] = True
                    elif board[nx][ny] == player and not visited[nx][ny]:
                        queue.append((nx, ny))
                        visited[nx][ny] = True

        return liberty

    def _remove_stones(self, x, y, player, captured_stones=None):
        """移除一组棋子"""
        if self.board[x][y] != player:
            return

        visited = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
        queue = [(x, y)]
        visited[x][y] = True

        while queue:
            cx, cy = queue.pop(0)
            self.board[cx][cy] = 0  # 移除棋子
            if captured_stones is not None:
                captured_stones.append((cx, cy))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.board[nx][ny] == player and not visited[nx][ny]:
                        queue.append((nx, ny))
                        visited[nx][ny] = True

    def _update_liberty_board(self):
        """更新气数棋盘"""
        self.liberty_board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]

        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] != 0:
                    self.liberty_board[x][y] = self._calculate_liberty(self.board, x, y, self.board[x][y])

    def _is_ko(self, temp_board, x, y):
        """检查是否是劫争"""
        # 如果历史记录为空，不可能是劫
        if not self.history_boards:
            return False

        # 检查当前局面是否与两步前相同（劫争）
        if len(self.history_boards) >= 2:
            prev_board = self.history_boards[-2]
            if self._boards_equal(temp_board, prev_board):
                return True

        return False

    def _boards_equal(self, board1, board2):
        """比较两个棋盘是否相同"""
        for x in range(self.board_size):
            for y in range(self.board_size):
                if board1[x][y] != board2[x][y]:
                    return False
        return True

    def _is_eye(self, x, y, player):
        """判断是否形成眼"""
        # 简单判断：周围四个方向都是己方棋子
        if self.board[x][y] != player:
            return False

        count = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if self.board[nx][ny] == player:
                    count += 1

        return count >= 3  # 简单判断，实际眼的判断更复杂

    def _determine_winner(self):
        """确定胜负（数子法）"""
        # 简化版胜负判断，实际围棋计分更复杂
        black_territory = 0
        white_territory = 0

        # 简单计算：黑子数 vs 白子数 + 贴目
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 1:
                    black_territory += 1
                elif self.board[x][y] == 2:
                    white_territory += 1

        white_territory += self.komi  # 加上贴目

        if black_territory > white_territory:
            self.winner = 1
        elif white_territory > black_territory:
            self.winner = 2
        else:
            self.winner = 0  # 和棋

    def check_win(self, x, y):
        """围棋没有连续五个的胜利条件，游戏结束由双方连续pass决定"""
        return self.game_over