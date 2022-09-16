import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Modal from 'react-bootstrap/Modal';
import { Link, useParams } from "react-router-dom";
import { Col, ListGroup, ListGroupItem, Row, Form, Footer } from 'react-bootstrap';
import NavBar from '../components/navbar';
import Profile from '../components/profile';
import ProblemList from '../components/problem_list';
import Ranking from '../components/ranking';
import useToken from '../useTokens';
import { useEffect, useState } from 'react';
import Board from '../components/chess_board';


function ViewPlayOption() {

    const { token, setToken } = useToken();

    const [showCustom, setshowCustom] = useState(false);
    const [showFindMatch, setshowFindMatch] = useState(false);
    const [showBot, setshowBot] = useState(false);
    const [matchID, setMatchID] = useState(0);

    const handleCustom = () => setshowCustom(true);
    const handleCancelCustom = () => setshowCustom(false);

    const handleFindingMatch = () => setshowFindMatch(true);
    const handleCancelFinding = () => setshowFindMatch(false);

    const handleBot = () => setshowBot(true);
    const handleCancelBot = () => setshowBot(false);

    const handleCreateRoom = async (e) => {
        e.preventDefault();
        const res = await fetch(`http://localhost:8000/api/match/add/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: token.username
            })
        });
        const data = await res.json();

        if(data.status === "failed") {
            alert(data.reason);
            window.location.reload();
            return;
        }
        alert("Successful");
        window.location.reload();
    }

    const handleMatchIDChange = (e) => setMatchID(e.target.value);

    const handleJoinRoom = async (e) => {
        e.preventDefault();
        console.log(token);
        const res = await fetch(`http://localhost:8000/api/match/join/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: token.username,
                password: token.password,
                match_id: matchID
            })
        });
        const data = await res.json();

        if(data.status === "failed") {
            alert(data.reason);
            window.location.reload();
            return;
        }

        alert("Successful");
        window.location.reload();
    }

    return (
        <>
            <Modal show={showCustom} onHide={handleCancelCustom}>
                <Modal.Header closeButton>
                    <Modal.Title>Custom match</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Row>
                        <Col sm={6}>
                            <Form onSubmit={handleCreateRoom}>
                                <center>
                                    <Button style={{marginTop: "10%"}} variant="primary" type="submit">
                                        Create custom room
                                    </Button>
                                </center>
                            </Form>
                        </Col>

                        <Col sm={6}>
                            <Form onSubmit={handleJoinRoom}>
                                <Form.Group className="mb-3" controlId="formBasicUsername">
                                    <Form.Control onChange={handleMatchIDChange} type="number" placeholder="Enter ID" />
                                </Form.Group>
                                <center>
                                    <Button variant="primary" type="submit">
                                        Join
                                    </Button>
                                </center>
                            </Form>
                        </Col>
                        
                    </Row>
                </Modal.Body>
            </Modal>

            <Modal show={showFindMatch} onHide={handleCancelFinding}>
                <Modal.Header closeButton>
                    <Modal.Title>Finding a match...</Modal.Title>
                </Modal.Header>
                <Modal.Footer>
                    <Button variant="danger" onClick={handleCancelFinding}>
                        Cancel
                    </Button>
                </Modal.Footer>
            </Modal>

            <Modal show={showBot} onHide={handleCancelBot}>
                <Modal.Header closeButton>
                    <Modal.Title>Play with bot</Modal.Title>
                </Modal.Header>
                <Modal.Footer>
                    <Button variant="danger" onClick={handleCancelBot}>
                        Cancel
                    </Button>
                </Modal.Footer>
            </Modal>

            <NavBar/>

            <br/>

            <Container>
                <Row>
                    <Col sm={9}>
                        <center>
                            <h1>Play</h1>
                        </center>
                        <Row>
                            <Col sm={4}>
                                <center>
                                <Card style={{ width: "40%", height: "5rem" }} onClick={handleCustom}>
                                    <Button variant="success" style={{height: "100%"}}><b>Custom match</b></Button>
                                </Card>
                                </center>
                            </Col>
                            <Col sm={4}>
                                <center>
                                <Card style={{ width: "40%", height: "5rem" }} onClick={handleFindingMatch}>
                                    <Button variant="success" style={{height: "100%"}}><b>Random matching</b></Button>
                                </Card>
                                </center>
                            </Col>
                            <Col sm={4}>
                                <center>
                                <Card style={{ width: "40%", height: "5rem" }} onClick={handleBot}>
                                    <Button variant="success" style={{height: "100%"}}><b>Play with bots</b></Button>
                                </Card>
                                </center>
                            </Col>
                        </Row>
                    </Col>

                    <Col sm={3}>
                        <Profile/>
                        <Ranking/>
                    </Col>
                </Row>
                
            </Container>
        </>
    );
}

function ShowBoard({userInfo}) {
    
    const { token, setToken } = useToken();
    const [info, setInfo] = useState({});
    const [matchInfo, setMatchInfo] = useState({});

    const [socket, setSocket] = useState(new WebSocket("ws://localhost:8000/ws/resign/1/"));

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if(data.player === token.username) return;
        alert("Your opponent resigns");
        window.location.reload();
    };

    socket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    useEffect(() => {
        let ignore = false;
        async function fetchData() {
            if(!token) return;
            if(ignore) return;
            if(!userInfo.in_game) return;

            const match = await fetch(`http://localhost:8000/api/match/${userInfo.in_game}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const match_data = await match.json();
            const white_player = await (await fetch(match_data.white_player, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })).json();

            const black_player = (match_data.black_player)? await (await fetch(match_data.black_player, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })).json() : null;
            setMatchInfo({
                id: match_data.id,
                fen: match_data.fen,
                white_player: white_player.username,
                white_points: match_data.white_points,
                white_elo: white_player.elo,
                black_player: (black_player)? black_player.username : null,
                black_points: match_data.black_points,
                black_elo: (black_player)? black_player.elo : null,
                my_points: (token.username === white_player.username)? match_data.white_points : match_data.black_points
            });
            
        }

        fetchData();
        return () => { ignore = true; }        
    }, []);

    const resign = async (e) => {
        const res = await fetch(`http://localhost:8000/api/match/resign/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: token.username,
                password: token.password,
                match_id: matchInfo.id
            })
        });
        const data = await res.json();

        if(data.status === "failed") {
            alert(data.reason);
            window.location.reload();
            return;
        }
        socket.send(JSON.stringify({
            'player': token.username
        }));
        alert("Successful");
        window.location.reload();
    }

    return (
        <>
            <NavBar/>

            <br/>

            <Container>
                <Row>
                    <Col id="board_area" sm={8}>
                        {
                            (matchInfo.black_player)? 
                                <Board matchInfo={matchInfo} userInfo={userInfo}/>
                            :
                                <center>
                                    <h3>Waiting for another player...</h3>
                                </center>
                        }
                    </Col>

                    <Col sm={4}>
                        <Card style={{ width: "70%", margin: '10px' }} >
                            <Card.Header>
                                Match details
                                <Button variant="danger" style={{ float: "right"}} onClick={resign}><b>Resign</b></Button>
                            </Card.Header>
                            <Card.Body>
                                <Card.Text> Match ID: {matchInfo.id} </Card.Text>
                                <Card.Text> White player: {matchInfo.white_player} ({matchInfo.white_elo})</Card.Text>
                                <Card.Text> Black player: {matchInfo.black_player} ({matchInfo.black_elo})</Card.Text> 
                                <Card.Text> Status: white to move </Card.Text> 
                                <center>
                                    <Card.Text> Your Points: {matchInfo.my_points} </Card.Text>
                                    <Button>Roll</Button>
                                </center>
                                <br></br>
                                <Card.Text style={{ fontSize: "small" }}> Win (+102) / Lose (-13) / Draw (-1) </Card.Text> 
                            </Card.Body>
                        </Card>

                        <Card style={{ width: "70%", height: "20rem", margin: '10px' }} >
                            <Card.Header>Move history</Card.Header>
                            <Card.Body style={{ overflow: "auto" }}>
                                <Card.Text>1</Card.Text>
                                <Card.Text>2</Card.Text>
                                <Card.Text>3</Card.Text>
                                <Card.Text>4</Card.Text>
                                <Card.Text>5</Card.Text>
                                <Card.Text>6</Card.Text>
                                <Card.Text>7</Card.Text>
                                <Card.Text>8</Card.Text>
                                <Card.Text>9</Card.Text>
                                <Card.Text>10</Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
                
            </Container>
        </>
    )
}


function Play() {

    const { token, setToken } = useToken();
    const [info, setInfo] = useState({});
    const [matchInfo, setMatchInfo] = useState({});

    useEffect(() => {
        let ignore = false;

        async function fetchData() {
            if(!token) return;
            if(ignore) return;
            const user = await fetch(`http://localhost:8000/api/user/getinfo/?username=${token.username}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const user_data = await user.json();
            setInfo({
                username: user_data.username,
                in_game: user_data.in_game,
                number_of_matches: user_data.number_of_matches,
                elo: user_data.elo
            });
        }

        fetchData();
        return () => { ignore = true; }        
    }, []);

    return (
        <div>
            {
                (info.in_game)? 
                    <ShowBoard userInfo={info}/>
                :
                    <ViewPlayOption/>
            }
        </div>
    )
    
}

export default Play;