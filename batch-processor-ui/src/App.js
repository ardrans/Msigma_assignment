import React, { useState } from 'react';
import { Nav, Container } from 'react-bootstrap';
import './App.css';
import FormPage from './components/FormPage';
import RecordsList from './components/RecordsList';

function App() {
  const [activeTab, setActiveTab] = useState('form');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Batch Processing Portal</h1>
        <p className="App-subtitle">Submit and track records for batch processing</p>
      </header>

      <Container className="py-3">
        <Nav variant="pills" className="justify-content-center mb-4">
          <Nav.Item>
            <Nav.Link
              active={activeTab === 'form'}
              onClick={() => setActiveTab('form')}
              className="nav-pill"
            >
              Submit Record
            </Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link
              active={activeTab === 'records'}
              onClick={() => setActiveTab('records')}
              className="nav-pill"
            >
              View Processed Records
            </Nav.Link>
          </Nav.Item>
        </Nav>
      </Container>

      <main className="App-main">
        {activeTab === 'form' ? <FormPage /> : <RecordsList />}
      </main>
    </div>
  );
}

export default App;
