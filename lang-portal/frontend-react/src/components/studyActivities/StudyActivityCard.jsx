import React from 'react';
import { Link } from 'react-router-dom';

function StudyActivityCard({ activity }) {
  return (
    <div className="study-activity-card">
      <img 
        src={activity.thumbnail_url} 
        alt={activity.name} 
        className="activity-thumbnail"
      />
      <h3>{activity.name}</h3>
      <div className="card-actions">
        <Link 
          to={`/study_activities/${activity.id}/launch`}
          className="launch-button"
        >
          Launch
        </Link>
        <Link 
          to={`/study_activities/${activity.id}`}
          className="view-button"
        >
          View Details
        </Link>
      </div>
    </div>
  );
}

export default StudyActivityCard; 