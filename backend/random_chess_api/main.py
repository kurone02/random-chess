from stockfish import Stockfish
from gacha_chess import GachaChess
import ultils
from monte_carlo_search import MonteCarloEngine

if __name__ == "__main__":

    # game = GachaChess()
    stockfish = Stockfish("/usr/games/stockfish")
    stockfish.set_elo_rating(1500)

    # while not game.is_over():
    #     engine = MonteCarloEngine(game)
    #     move_info = engine.get_best_move(50)
    #     print(move_info)
    #     if move_info.split()[0] == "SET":
    #         game.white_player.points -= game.GACHA_PRICE
    #     game.move(move_info)
    #     if game.is_over():
    #         break
    #     stockfish.set_fen_position(game.board.fen())
    #     move_info = stockfish.get_best_move()
    #     print(move_info)
    #     game.move(move_info)
    #     print(game)
    
    # print(game.get_result())
    

    for _ in range(1):
        print(f"Game {_ + 1}:")
        game = GachaChess()
        # print(game)
        # os.system("clear")
        while not game.is_over():
            legal_moves = game.legal_moves()
            move_info = legal_moves[ultils.rand(0, len(legal_moves) - 1)]
            if move_info.split()[0] == "SET":
                game.current_player().points -= game.GACHA_PRICE
            game.move(move_info)
            print(move_info)
            print(game)
            # sleep(0.1)
            # os.system("clear")
        print(game)
        print(game.board.fen())
        result = game.get_result()
        if result == "Draw":
            print("Draw by", game.get_draw_reason())
        else:
            print(result)
        stockfish.set_fen_position(game.board.fen())
        # value = stockfish.get_evaluation()["value"]
        print(f"Board evaluation: {stockfish.get_evaluation()}")

        print('-' * 35)
