
import { useEffect, useState } from "react";
import { Container, Spinner } from "react-bootstrap";
import { Col, Row, Table } from 'react-bootstrap';
import NavBar from '../components/navbar';
import Profile from '../components/profile';
import Ranking from '../components/ranking';

function Leaderboard() {

    // const [data, setData] = useState(0);
    // const [rank, setRank] = useState({i: 0});
    // async function get_accounts() {
    //     const res = await fetch("http://localhost:2022/accounts");
    //     const acc = await res.json();
    //     setData(acc);
    // }
    // useEffect(() => {
    //     console.log(data, !!data.accounts);
    //     if(data.accounts) return;
    //     get_accounts();
    // }, []);

    // console.log(data);

    // if(!data.accounts) return false;

    // let i = 1;
    // let leaderboard = data.accounts.map((acc) => {
    //     i++;
    //     return (
    //         <tr>
    //             <td>{i}</td>
    //             <td>Admin</td>
    //             <td>3</td>
    //             <td>309</td>
    //         </tr>
    //     )
    // });

    return (
        <>
            <NavBar/>

            <br/>

            <Container>
            <Spinner/>
                <Row>
                    <Col sm={9}>
                        <center>
                            <h1>Leaderboard</h1>
                        </center>
                        <Table striped bordered hover>
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Username</th>
                                    <th>Problem sovled</th>
                                    <th>Total coins</th>
                                </tr>
                            </thead>
                            <tbody>
                                
                                <tr>
                                    <td>1</td>
                                    <td>Admin</td>
                                    <td>3</td>
                                    <td>309</td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>Tester01</td>
                                    <td>5</td>
                                    <td>15</td>
                                </tr>
                                <tr>
                                    <td>3</td>
                                    <td>Tester02</td>
                                    <td>4</td>
                                    <td>12</td>
                                </tr>
                                <tr>
                                    <td>4</td>
                                    <td>Tester03</td>
                                    <td>3</td>
                                    <td>9</td>
                                </tr>
                                <tr>
                                    <td>5</td>
                                    <td>Tester04</td>
                                    <td>2</td>
                                    <td>6</td>
                                </tr>
                                <tr>
                                    <td>6</td>
                                    <td>Tester05</td>
                                    <td>1</td>
                                    <td>3</td>
                                </tr>
                                <tr>
                                    <td>7</td>
                                    <td>Tester06</td>
                                    <td>0</td>
                                    <td>0</td>
                                </tr>
                                <tr>
                                    <td>8</td>
                                    <td>Tester07</td>
                                    <td>0</td>
                                    <td>0</td>
                                </tr>
                                <tr>
                                    <td>9</td>
                                    <td>Tester08</td>
                                    <td>0</td>
                                    <td>0</td>
                                </tr>
                                <tr>
                                    <td>10</td>
                                    <td>Tester09</td>
                                    <td>0</td>
                                    <td>0</td>
                                </tr>
                                
                                
                            </tbody>
                        </Table>
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

export default Leaderboard;