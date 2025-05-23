'''
游戏工厂类
功能：根据用户选择创建不同类型的游戏实例
'''

from .game_gomoku import GomokuGame
from .game_go import GoGame

class BoardGameFactory:
    @staticmethod
    def create_game(game_type, board_size=None):
        """创建游戏实例"""
        if game_type == "gomoku":
            # 五子棋默认15x15
            size = board_size if board_size is not None else 15
            return GomokuGame(board_size=size)
        elif game_type == "go":
            # 围棋默认19x19
            size = board_size if board_size is not None else 19
            return GoGame(board_size=size)
        else:
            raise ValueError(f"不支持的游戏类型: {game_type}")