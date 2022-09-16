from __future__ import annotations
from math import inf, log, sqrt
import chess
from stockfish import Stockfish
from gacha_chess import GachaChess
import ultils

class TreeNode:
    WINNING_POINT = 1000000
    CENTIPAWN = 100

    def __init__(self, state: GachaChess=GachaChess(), score: float=0, n_visits: int=0) -> None:
        self.state = state
        self.score = score
        self.parent: TreeNode = None
        self.n_visits = n_visits
        self.children: list[(TreeNode, str)] = []

    def UCB1(self, constant=2) -> float:
        if self.n_visits == 0:
            return inf
        if self.parent == None:
            return self.score
        return self.score + constant * sqrt(log(self.parent.n_visits) / self.n_visits)

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def find_max_child(self) -> TreeNode:
        chosen_child: TreeNode = None
        for current_child in self.children:
            current_child = current_child[0]
            if chosen_child is None:
                chosen_child = current_child
            if chosen_child.UCB1(self.n_visits) < current_child.UCB1(self.n_visits):
                chosen_child = current_child
        return chosen_child

    def get_best_child(self) -> str:
        chosen_child: TreeNode = None
        chosen_move: str = ""
        for current_child in self.children:
            if chosen_child is None:
                chosen_child = current_child[0]
                chosen_move = current_child[1]
            if chosen_child.score < current_child[0].score:
                chosen_child = current_child[0]
                chosen_move = current_child[1]
        return chosen_move

    def rollout(self, depth=50) -> int:
        game = self.state.copy()
        for _ in range(depth):
            if game.is_over():
                break
            legal_moves = game.legal_moves()
            move_info = legal_moves[ultils.rand(0, len(legal_moves) - 1)]
            if move_info.split()[0] == "SET":
                game.current_player().points -= game.GACHA_PRICE
            game.move(move_info)
        if game.is_draw():
            return 0
        if not game.is_checkmate():
            stockfish = Stockfish("/usr/games/stockfish")
            stockfish.set_elo_rating(2000)
            stockfish.set_fen_position(game.board.fen())
            evaluation = stockfish.get_evaluation()
            print(evaluation)
            if evaluation["type"] == "mate":
                return self.WINNING_POINT if evaluation["value"] > 0 else -self.WINNING_POINT
            return evaluation["value"] / self.CENTIPAWN
        if game.current_turn == chess.BLACK:
            return self.WINNING_POINT
        return -self.WINNING_POINT

    def expand(self) -> None:
        legal_moves = self.state.legal_moves()
        for move_info in legal_moves:
            game = self.state.copy()
            if move_info.split()[0] == "SET":
                game.current_player().points -= game.GACHA_PRICE
            game.move(move_info)
            new_node = TreeNode(game.copy(), 0, 0)
            new_node.parent = self
            self.children.append((new_node, move_info))
    
    def backpropagation(self, score) -> None:
        current_node = self
        while current_node is not None:
            current_node.score += score
            current_node.n_visits += 1
            current_node = current_node.parent


class MonteCarloEngine:

    def __init__(self, state: GachaChess) -> None:
        self.root = TreeNode(state.copy())

    
    def refine(self) -> None:
        current_node = self.root
        if not current_node.is_leaf():
            current_node = current_node.find_max_child()
        if current_node.n_visits != 0:
            current_node.expand()
            current_node = current_node.children[0][0]
        terminated_value = current_node.rollout()
        if terminated_value != 0:
            current_node.backpropagation(terminated_value)

    def search(self, max_iter=100) -> None:
        for iter in range(max_iter):
            self.refine()

    def get_best_move(self, max_iter=100):
        self.search(max_iter)
        return self.root.get_best_child()
