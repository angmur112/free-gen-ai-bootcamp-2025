import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import StudyActivities from './pages/StudyActivities';
import StudyActivityShow from './pages/StudyActivityShow';
import StudyActivityLaunch from './pages/StudyActivityLaunch';
import Words from './pages/Words';
import WordShow from './pages/WordShow';
import Groups from './pages/Groups';
import GroupShow from './pages/GroupShow';
import StudySessions from './pages/StudySessions';
import StudySessionShow from './pages/StudySessionShow';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/study_activities" element={<StudyActivities />} />
        <Route path="/study_activities/:id" element={<StudyActivityShow />} />
        <Route path="/study_activities/:id/launch" element={<StudyActivityLaunch />} />
        <Route path="/words" element={<Words />} />
        <Route path="/words/:id" element={<WordShow />} />
        <Route path="/groups" element={<Groups />} />
        <Route path="/groups/:id" element={<GroupShow />} />
        <Route path="/study_sessions" element={<StudySessions />} />
        <Route path="/study_sessions/:id" element={<StudySessionShow />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Router>
  );
}

export default App; 