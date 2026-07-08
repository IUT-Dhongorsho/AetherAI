import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import PatientIntake from './pages/PatientIntake';
import TriageResults from './pages/TriageResults';

function App() {
  return (
    <Router basename="/aetherai">
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/intake" replace />} />
          <Route path="intake" element={<PatientIntake />} />
          <Route path="results" element={<TriageResults />} />
          <Route path="analysis" element={<div className="p-xl text-center">Placeholder for Analysis View</div>} />
          <Route path="history" element={<div className="p-xl text-center">Placeholder for History View</div>} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
