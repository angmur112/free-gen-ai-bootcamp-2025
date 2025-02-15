import React from 'react';

function StudyProgress({ data }) {
  if (!data) return null;

  const masteryPercentage = (data.mastery_progress * 100).toFixed(1);
  const progressText = `${data.total_words_studied}/${data.total_words}`;

  return (
    <div className="study-progress">
      <h2>Study Progress</h2>
      <div className="progress-details">
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${masteryPercentage}%` }}
          />
        </div>
        <p>Words Studied: {progressText}</p>
        <p>Mastery: {masteryPercentage}%</p>
      </div>
    </div>
  );
}

export default StudyProgress; 