import React from 'react';
import { Link } from 'react-router-dom';

function LastStudySession({ data }) {
  if (!data) return null;

  return (
    <div className="last-study-session">
      <h2>Last Study Session</h2>
      <div className="session-details">
        <p>Activity: {data.activity_name}</p>
        <p>Last Used: {new Date(data.last_used).toLocaleDateString()}</p>
        <div className="results-summary">
          <span>Correct: {data.correct_count}</span>
          <span>Wrong: {data.wrong_count}</span>
        </div>
        <Link to={`/groups/${data.group_id}`}>View Group</Link>
      </div>
    </div>
  );
}

export default LastStudySession; 