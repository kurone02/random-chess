import { useState, useEffect } from "react";
import Chess from "../ultils/chess.js";
import { Chessboard } from "react-chessboard";

export default function Board() {
    const [game, setGame] = useState(new Chess("ppppkppp/pppppppp/8/8/8/8/PPPPPPPP/PPPPKPPP w - - 0 1"));
    const [chessboardSize, setChessboardSize] = useState(undefined);

    useEffect(() => {
        function handleResize() {
            const display = document.getElementById("board_area");
            setChessboardSize(display.offsetWidth - 20);
        }

        window.addEventListener("resize", handleResize);
        handleResize();
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    function makeAMove(move) {
        const gameCopy = {...game};
        const result = gameCopy.move(move);
        console.log(game);
        setGame(gameCopy);
        console.log(move);
        console.log(result);
        return result; // null if the move was illegal, the move object if the move was legal
    }

    function makeRandomMove() {
        const possibleMoves = game.moves();
        // exit if the game is over
        if (game.game_over() || game.in_draw() || possibleMoves.length === 0) return;
        const randomIndex = Math.floor(Math.random() * possibleMoves.length);
        makeAMove(possibleMoves[randomIndex]);
    }

    function onDrop(sourceSquare, targetSquare) {
        const move = makeAMove({
            from: sourceSquare,
            to: targetSquare,
            promotion: 'q' // always promote to a queen for example simplicity
        });

        // illegal move
        if (move === null) return false;

        setTimeout(makeRandomMove, 200);
        return true;
    }

    return <Chessboard boardWidth={chessboardSize} position={game.fen()} onPieceDrop={onDrop} />;
}