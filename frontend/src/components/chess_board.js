import { useRef, useState, useEffect } from 'react';
import Chess from '../ultils/chess.js';

import { Chessboard } from 'react-chessboard';

export default function SquareStyles({matchInfo, userInfo}) {
    const chessboardRef = useRef();
    const [game, setGame] = useState(new Chess(matchInfo.fen));
    const [orientation, setOrientation] = useState((matchInfo.white_player === userInfo.username)? "white" : "black");
    const [playerTurn, setPlayerTurn] = useState((matchInfo.white_player === userInfo.username)? "w" : "b");

    const [chessboardSize, setChessboardSize] = useState(undefined);
    const socket = useRef({});

    useEffect(() => {
        function handleResize() {
            const display = document.getElementById("board_area");
            setChessboardSize(display.offsetWidth * 0.8);
        }

        window.addEventListener("resize", handleResize);
        handleResize();
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    useEffect(() => {
        let ignore = false;

        function makeAMove(move, data) {
            const gameCopy = { ...game };
            const result = gameCopy.move(move);
            setGame(gameCopy);
            setMoveSquares({
                [data.move.from]: { backgroundColor: 'rgba(255, 255, 0, 0.4)' },
                [data.move.to]: { backgroundColor: 'rgba(255, 255, 0, 0.4)' }
            });
            return result; // null if the move was illegal, the move object if the move was legal
        }

        async function fetchData() {
            if(ignore) return;

            socket.move = new WebSocket(`ws://localhost:8000/ws/move/${matchInfo.id}/`);
            socket.move.onmessage = function(e) {
                const data = JSON.parse(e.data);
                if(data.player === userInfo.username) return;
                console.log(data);
                makeAMove(data.move, data);
            };
        
            socket.move.onclose = function(e) {
                console.error('Chat socket closed unexpectedly');
            };
            
        }

        fetchData();
        return () => { ignore = true; }        
    }, []);

    const [rightClickedSquares, setRightClickedSquares] = useState({});
    const [moveSquares, setMoveSquares] = useState({});
    const [optionSquares, setOptionSquares] = useState({});

    function onDrop(sourceSquare, targetSquare) {
        if(playerTurn !== game.turn()) return;
        const gameCopy = { ...game };
        const move = gameCopy.move({
            from: sourceSquare,
            to: targetSquare,
            promotion: 'q' // always promote to a queen for example simplicity
        });
        setGame(gameCopy);
        // illegal move
        if (move === null) return false;
        setMoveSquares({
            [sourceSquare]: { backgroundColor: 'rgba(255, 255, 0, 0.4)' },
            [targetSquare]: { backgroundColor: 'rgba(255, 255, 0, 0.4)' }
        });
        socket.move.send(JSON.stringify({
            'player': userInfo.username,
            'fen': game.fen(),
            'move': move
        }));
        return true;
    }

    function onMouseOverSquare(square) {
        if(playerTurn !== game.turn()) return;
        getMoveOptions(square);
    }

    // Only set squares to {} if not already set to {}
    function onMouseOutSquare() {
        if(playerTurn !== game.turn()) return;
        if (Object.keys(optionSquares).length !== 0) setOptionSquares({});
    }

    function getMoveOptions(square) {
        if(playerTurn !== game.turn()) return;
        const moves = game.moves({
            square,
            verbose: true
        });
        if (moves.length === 0) { return; }

        const newSquares = {};
        moves.map((move) => {
            newSquares[move.to] = {
                background:
                game.get(move.to) && game.get(move.to).color !== game.get(square).color
                    ? 'radial-gradient(circle, rgba(0,0,0,.1) 85%, transparent 85%)'
                    : 'radial-gradient(circle, rgba(0,0,0,.1) 25%, transparent 25%)',
                borderRadius: '50%'
            };
            return move;
        });
        newSquares[square] = { background: 'rgba(255, 255, 0, 0.4)' };
        setOptionSquares(newSquares);
    }

    function onSquareClick() {
        setRightClickedSquares({});
    }

    function onSquareRightClick(square) {
        const colour = 'rgba(0, 0, 255, 0.4)';
        setRightClickedSquares({
            ...rightClickedSquares,
            [square]:
                rightClickedSquares[square] && rightClickedSquares[square].backgroundColor === colour
                ? undefined
                : { backgroundColor: colour }
        });
    }

    return (
        <div>
        <Chessboard
            id="SquareStyles"
            animationDuration={200}
            boardWidth={chessboardSize}
            position={game.fen()}
            onMouseOverSquare={onMouseOverSquare}
            onMouseOutSquare={onMouseOutSquare}
            onSquareClick={onSquareClick}
            onSquareRightClick={onSquareRightClick}
            onPieceDrop={onDrop}
            customBoardStyle={{
                borderRadius: '4px',
                boxShadow: '0 5px 15px rgba(0, 0, 0, 0.5)'
            }}
            customSquareStyles={{
                ...moveSquares,
                ...optionSquares,
                ...rightClickedSquares
            }}
            boardOrientation={orientation}
            ref={chessboardRef}
        />
        </div>
    );
}