import React from 'react';

function QuickStats({ data }) {
  if (!data) return null;

  return (
    <div className="quick-stats">
      <h2>Quick Stats</h2>
      <div className="stats-grid">
        <div className="stat-item">
          <h3>Success Rate</h3>
          <p>{data.success_rate}%</p>
        </div>
        <div className="stat-item">
          <h3>Study Sessions</h3>
          <p>{data.total_study_sessions}</p>
        </div>
        <div className="stat-item">
          <h3>Active Groups</h3>
          <p>{data.total_active_groups}</p>
        </div>
        <div className="stat-item">
          <h3>Study Streak</h3>
          <p>{data.study_streak} days</p>
        </div>
      </div>
    </div>
  );
}

export default QuickStats; 