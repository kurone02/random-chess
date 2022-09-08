import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Modal from 'react-bootstrap/Modal';
import { Link, useParams } from "react-router-dom";
import { Col, ListGroup, ListGroupItem, Row, Form } from 'react-bootstrap';
import NavBar from '../components/navbar';
import Profile from '../components/profile';
import ProblemList from '../components/problem_list';
import Ranking from '../components/ranking';
import useToken from '../useTokens';
import { useState } from 'react';
import Board from '../components/chess_board';


function ViewProblemList() {

    const [showCustom, setshowCustom] = useState(false);
    const [showFindMatch, setshowFindMatch] = useState(false);
    const [showBot, setshowBot] = useState(false);

    const handleCustom = () => setshowCustom(true);
    const handleCancelCustom = () => setshowCustom(false);

    const handleFindingMatch = () => setshowFindMatch(true);
    const handleCancelFinding = () => setshowFindMatch(false);

    const handleBot = () => setshowBot(true);
    const handleCancelBot = () => setshowBot(false);

    return (
        <>
            <Modal show={showCustom} onHide={handleCancelCustom}>
                <Modal.Header closeButton>
                    <Modal.Title>Custom match</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Row>
                        <Col sm={6}>
                            <Form>
                                <center>
                                    <Button style={{marginTop: "10%"}} variant="primary" type="submit">
                                        Create custom room
                                    </Button>
                                </center>
                            </Form>
                        </Col>

                        <Col sm={6}>
                            <Form>
                                <Form.Group className="mb-3" controlId="formBasicUsername">
                                    <Form.Control type="number" placeholder="Enter ID" />
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

function ShowBoard() {
    return (
        <>
            <NavBar/>

            <br/>

            <Container>
                <Row>
                    <Col id="board_area" sm={6}>
                        <Board/>
                    </Col>

                    <Col sm={3}>
                        <Card style={{ width: "40%", height: "5rem" }} >
                            <Button variant="success" style={{height: "100%"}}><b>Custom match</b></Button>
                        </Card>
                    </Col>

                    <Col sm={3}>
                        <Profile/>
                        <Ranking/>
                    </Col>
                </Row>
                
            </Container>
        </>
    )
}


function Play() {

    return ShowBoard();
 
    return ViewProblemList();
    
}

export default Play;