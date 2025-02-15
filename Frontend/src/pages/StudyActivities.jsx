import React, { useEffect, useState } from 'react';
import api from '../services/api';
import StudyActivityCard from '../components/studyActivities/StudyActivityCard';

function StudyActivities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const data = await api.getStudyActivities();
        setActivities(data);
      } catch (error) {
        console.error('Error fetching study activities:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchActivities();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="study-activities">
      <h1>Study Activities</h1>
      <div className="activities-grid">
        {activities.map(activity => (
          <StudyActivityCard 
            key={activity.id} 
            activity={activity} 
          />
        ))}
      </div>
    </div>
  );
}

export default StudyActivities; 