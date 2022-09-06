import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Link } from "react-router-dom";
import { Col, Row } from 'react-bootstrap';
import NavBar from './components/navbar';
import Profile from './components/profile';
import Ranking from './components/ranking';

function App() {
    return (
        <>
            <NavBar/>

            <br/>

            <Container>
                <Row>
                    <Col sm={9}>
                        <center>
                            <h1>Announcement</h1>
                        </center>
                        <Row>
                            <Col sm={5}>
                                <Card style={{ width: '18rem' }}>
                                    <Card.Body>
                                        <Card.Title>How to use the website</Card.Title>
                                        <Card.Text>
                                            Firstly, you need to create an account. <br/>
                                            Then, you should sign in with your newly created account. <br/>
                                            Finally, navigate to the <a href="#problems">problems</a> site and start coding. <br/>
                                        </Card.Text>
                                        <Button variant="primary" href="/signup">Click here to sign up!</Button>
                                    </Card.Body>
                                </Card>

                                <br/>

                                <Card style={{ width: '18rem' }}>
                                    <Card.Body>
                                        <Card.Title>Welcome to UNICODE!</Card.Title>
                                        <Card.Text>
                                            This is a decentralized coding platform. <br/>
                                            Click the button below to start solving coding problems.
                                        </Card.Text>
                                        <Button variant="primary" href="/problems">Solve problems!</Button>
                                    </Card.Body>
                                </Card>
                            </Col>
                            <Col sm={4}>
                                <Card style={{ width: '18rem' }}>
                                    <Card.Body>
                                        <Card.Title>Lorem ipsum dolor sit amet</Card.Title>
                                        <Card.Text>
                                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                                        </Card.Text>
                                    </Card.Body>
                                </Card>
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

export default App;