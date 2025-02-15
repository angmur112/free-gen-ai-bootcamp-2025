import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import LastStudySession from '../components/dashboard/LastStudySession';
import StudyProgress from '../components/dashboard/StudyProgress';
import QuickStats from '../components/dashboard/QuickStats';

function Dashboard() {
  const [lastSession, setLastSession] = useState(null);
  const [progress, setProgress] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      const [lastSessionData, progressData, statsData] = await Promise.all([
        api.getLastStudySession(),
        api.getStudyProgress(),
        api.getQuickStats()
      ]);

      setLastSession(lastSessionData);
      setProgress(progressData);
      setStats(statsData);
    };

    fetchDashboardData();
  }, []);

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      <LastStudySession data={lastSession} />
      
      <StudyProgress data={progress} />
      
      <QuickStats data={stats} />
      
      <Link to="/study_activities" className="start-studying-button">
        Start Studying
      </Link>
    </div>
  );
}

export default Dashboard; 
 