from __future__ import annotations
from typing import List, Optional
from . import ultils
from .ultils import chess

class ChessPlayer:

    def __init__(self, color=chess.WHITE, points = 0) -> None:
        self.color = color
        self.points = points
        self.gacha_pieces = []
    

class GachaChess:
    GACHA_PRICE = 7

    def __init__(self, fen=ultils.DEFAULT_FEN, white_points=GACHA_PRICE, black_points=GACHA_PRICE-1) -> None:
        self.board = chess.Board(fen)
        self.history = []
        self.move_history = []
        self.white_player = ChessPlayer(color=chess.WHITE, points=white_points)
        self.black_player = ChessPlayer(color=chess.BLACK, points=black_points)

    def __str__(self) -> str:
        return f"{self.board.__str__()}\n{'-' * 16}\nWhite's point: {self.white_player.points}\nBlack's point: {self.black_player.points}"

    def increase_point(self, ammount: int=1) -> None:
        self.current_player().points += ammount

    def decrease_point(self, ammount: int=1) -> None:
        self.current_player().points -= ammount
    
    def move(self, move_info: str) -> bool:
        # token = [SET, square, piece]
        token = move_info.split()
        if token[0] == "SET":
            if token[2].islower() and self.current_turn() == chess.WHITE:
                return False
            if token[2].isupper() and self.current_turn() == chess.BLACK:
                return False
            if self.board.piece_at(chess.parse_square(token[1])).piece_type != chess.PAWN:
                return False
            self.history.append(self.board.fen())
            self.move_history.append(move_info)
            self.replace_pawn(chess.parse_square(token[1]), chess.Piece.from_symbol(token[2]))
            return True
        try:
            if self.board.is_capture(chess.Move.from_uci(move_info)):
                print("yo?")
                self.current_player().points += ultils.PIECE_POINTS[self.board.piece_at(chess.Move.from_uci(move_info).to_square).symbol().lower()]
            self.history.append(self.board.fen())
            self.move_history.append(move_info)
            self.board.push_san(move_info)
            self.increase_point()
            return True
        except:
            return False

    def undo(self) -> bool:
        if len(self.history) == 0:
            return False
        self.decrease_point()
        self.board.set_board_fen(self.history.pop())
        return True

    def legal_moves(self) -> List[str]:
        legal_moves = [x.__str__() for x in self.board.legal_moves]
        if self.current_player().points < self.GACHA_PRICE:
            return legal_moves
        if self.board.is_check():
            return legal_moves
        for sq in chess.SQUARE_NAMES:
            for new_piece in ultils.GACHA_LIST:
                square = chess.parse_square(sq)
                if self.board.piece_at(square) is None:
                    continue
                if self.board.piece_at(square).piece_type != chess.PAWN:
                    continue
                if self.board.piece_at(square).color != self.current_turn():
                    continue
                new_move = f"SET {sq} {new_piece.upper() if self.current_turn() == chess.WHITE else new_piece}"
                legal_moves.append(new_move)
        return legal_moves

    def get_random_piece(self) -> Optional[chess.Piece]:
        threshold = ultils.rand(1, ultils.SUM_WEIGHTED_PROB)
        total = 0
        last_piece = None
        for (piece, value) in ultils.WEIGHTED_PROBABILITY:
            total += value
            last_piece = piece
            if total >= threshold:
                return piece
        return last_piece

    def current_turn(self) -> chess.Color:
        return self.board.turn

    def current_player(self) -> ChessPlayer:
        if self.current_turn():
            return self.white_player
        return self.black_player

    def other_player(self) -> ChessPlayer:
        if self.current_turn():
            return self.black_player
        return self.white_player

    def gacha(self) -> Optional[chess.Piece]:
        current_player = self.current_player()
        if current_player.points < self.GACHA_PRICE:
            return None
        current_player.points -= self.GACHA_PRICE
        random_piece = self.get_random_piece()
        current_player.gacha_pieces.append(random_piece)
        return random_piece

    def skip_turn(self) -> None:
        tokens = self.board.fen().split()
        if tokens[1] == 'w':
            tokens[1] = 'b'
        else:
            tokens[1] = 'w'
        new_fen = ' '.join(tokens)
        # self.history.append(self.board.fen())
        self.board.set_fen(new_fen)
        self.increase_point()

    def replace_pawn(self, square: chess.Square, new_piece: chess.Piece) -> bool:
        replaced_piece = self.board.piece_at(square)
        if replaced_piece.piece_type != chess.PAWN:
            return False
        if replaced_piece.color != self.current_turn():
            return False
        if replaced_piece not in self.current_player().gacha_pieces:
            return False
        self.board.set_piece_at(square, new_piece)
        self.current_player().gacha_pieces.remove(replaced_piece)
        self.skip_turn()
        return True

    def replace_pawn_by_id(self, square: chess.Square, new_piece_id: int) -> bool:
        current_player = self.current_player()
        new_piece = current_player.gacha_pieces[new_piece_id]
        if new_piece_id < 0 or new_piece_id >= len(current_player.gacha_pieces):
            return False
        self.replace_pawn(square, new_piece)

    def is_checkmate(self) -> bool:
        return self.board.is_checkmate()

    def is_repetition(self) -> bool:
        return self.board.is_repetition()

    def is_seventyfive_moves(self) -> bool:
        return self.board.is_seventyfive_moves()

    def is_stalemate(self) -> bool:
        return self.board.is_stalemate()

    def is_insufficient_material(self) -> bool:
        return self.board.is_insufficient_material()

    def get_draw_reason(self) -> str:
        if self.is_stalemate():
            return "Stalemate"
        if self.is_insufficient_material():
            return "Insufficient material"
        if self.is_repetition():
            return "Repetition"
        if self.is_seventyfive_moves():
            return "Seventy-five moves rule"
        return "Not draw"
        
    def is_draw(self) -> bool:
        return self.is_stalemate() or self.is_insufficient_material() or self.is_repetition() or self.is_seventyfive_moves()
    
    def is_over(self) -> bool:
        return self.is_checkmate() or self.is_draw()
    
    def get_result(self) -> str:
        if self.is_draw():
            return "Draw"
        if self.is_checkmate():
            return "White wins" if self.current_turn() == chess.BLACK else "Black wins"
        return "Ongoing"

    
    def copy(self) -> GachaChess:
        return GachaChess(
            fen=self.board.fen(),
            white_points=self.white_player.points,
            black_points=self.black_player.points
        )