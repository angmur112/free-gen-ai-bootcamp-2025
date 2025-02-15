import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';

function StudyActivityShow() {
  const { id } = useParams();
  const [activity, setActivity] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchActivityData = async () => {
      try {
        const [activityData, sessionsData] = await Promise.all([
          api.getStudyActivity(id),
          api.getStudyActivitySessions(id)
        ]);
        setActivity(activityData);
        setSessions(sessionsData);
      } catch (error) {
        console.error('Error fetching activity data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchActivityData();
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (!activity) return <div>Activity not found</div>;

  return (
    <div className="study-activity-show">
      <h1>{activity.name}</h1>
      <img 
        src={activity.thumbnail_url} 
        alt={activity.name} 
        className="activity-thumbnail"
      />
      <p className="activity-description">{activity.description}</p>
      
      <h2>Past Study Sessions</h2>
      <table className="sessions-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Group</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Review Items</th>
          </tr>
        </thead>
        <tbody>
          {sessions.map(session => (
            <tr key={session.id}>
              <td>{session.id}</td>
              <td>{session.group_name}</td>
              <td>{new Date(session.start_time).toLocaleString()}</td>
              <td>{new Date(session.end_time).toLocaleString()}</td>
              <td>{session.review_items_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default StudyActivityShow; 