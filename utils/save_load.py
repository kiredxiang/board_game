'''
保存和加载游戏状态的类 (SaveLoadManager)
功能：提供保存和加载游戏状态的功能。
'''
import json
from game_logic.game_gomoku import GomokuGame


class SaveLoadManager:
    def save_game(self, game, file_path):
        """将游戏状态保存到文件"""
        game_state = {
            'board_size': game.board_size,
            'board': game.board,
            'current_player': game.current_player,
            'move_history': game.move_history,
            'game_over': game.game_over,
            'winner': game.winner,
            'game_type': 'gomoku'  # 目前只支持五子棋
        }

        with open(file_path, 'w') as f:
            json.dump(game_state, f, indent=4)

    def load_game(self, file_path):
        """从文件加载游戏状态"""
        with open(file_path, 'r') as f:
            game_state = json.load(f)

        # 检查游戏类型
        if game_state.get('game_type') != 'gomoku':
            raise ValueError("不支持的游戏类型")

        # 创建游戏实例
        game = GomokuGame(board_size=game_state['board_size'])

        # 恢复游戏状态
        game.board = game_state['board']
        game.current_player = game_state['current_player']
        game.move_history = game_state['move_history']
        game.game_over = game_state['game_over']
        game.winner = game_state['winner']

        return game