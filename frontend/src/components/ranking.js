import { Table, Card } from "react-bootstrap";


export default function Ranking() {
    return (
        <Card style={{ width: '15rem', margin: '10px' }}>
            <Card.Header>Top players</Card.Header>
            <Table>
                <thead>
                    <tr>
                    <th>#</th>
                    <th>Username</th>
                    <th>Elo</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <td>1</td>
                    <td>Admin</td>
                    <td>309</td>
                    </tr>
                    <tr>
                    <td>2</td>
                    <td>Tester01</td>
                    <td>15</td>
                    </tr>
                    <tr>
                    <td>3</td>
                    <td>Tester02</td>
                    <td>12</td>
                    </tr>
                    <tr>
                    <td>4</td>
                    <td>Tester03</td>
                    <td>9</td>
                    </tr>
                    <tr>
                    <td>5</td>
                    <td>Tester04</td>
                    <td>6</td>
                    </tr>
                </tbody>
                </Table>
        </Card>
    )
}