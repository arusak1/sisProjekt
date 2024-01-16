import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import ScanResults from './ScanResults';
import ScanAll from './ScanAll';

const App = () => {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/ScanAllPage">Scan all</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/ScanAllPage" element={<ScanAll />} />
          <Route path="/" element={<ScanResults />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
