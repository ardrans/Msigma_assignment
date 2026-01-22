import React, { useState, useEffect } from 'react';
import { Table, Card, Spinner, Alert, Container, Badge } from 'react-bootstrap';
import './RecordsList.css';
import { getSuccessRecords } from '../services/api';

const RecordsList = () => {
    const [records, setRecords] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchRecords = async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getSuccessRecords();
            setRecords(result.data || []);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRecords();
    }, []);

    if (loading) {
        return (
            <Container className="text-center py-5">
                <Spinner animation="border" variant="light" />
                <p className="mt-3 text-white">Loading records...</p>
            </Container>
        );
    }

    if (error) {
        return (
            <Container>
                <Alert variant="danger">
                    {error}
                    <button className="btn btn-link" onClick={fetchRecords}>
                        Retry
                    </button>
                </Alert>
            </Container>
        );
    }

    return (
        <Card className="records-card">
            <Card.Body>
                <Card.Title className="d-flex justify-content-between align-items-center mb-4">
                    <h3>Processed Records</h3>
                    <Badge bg="success">{records.length} Records</Badge>
                </Card.Title>

                {records.length === 0 ? (
                    <div className="text-center py-4">
                        <p className="text-muted mb-0">No records with SUCCESS status yet.</p>
                    </div>
                ) : (
                    <div className="table-responsive">
                        <Table hover className="records-table mb-0">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Phone</th>
                                    <th>Link</th>
                                    <th>DOB</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {records.map((record) => (
                                    <tr key={record.id}>
                                        <td>{record.id}</td>
                                        <td>{record.name}</td>
                                        <td>{record.email}</td>
                                        <td>{record.phone_number}</td>
                                        <td>
                                            {record.link ? (
                                                <a href={record.link} target="_blank" rel="noopener noreferrer">
                                                    View
                                                </a>
                                            ) : (
                                                <span className="text-muted">-</span>
                                            )}
                                        </td>
                                        <td>{record.dob || <span className="text-muted">-</span>}</td>
                                        <td>
                                            <Badge bg="success">SUCCESS</Badge>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </Table>
                    </div>
                )}
            </Card.Body>
        </Card>
    );
};

export default RecordsList;
