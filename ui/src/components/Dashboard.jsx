import React, { useState, useEffect } from 'react';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalWords: 12450,
    dailyGoal: 500,
    wordsToday: 287,
    currentStreak: 15,
    lastSave: '2 hours ago'
  });

  const [recentActivity, setRecentActivity] = useState([
    { id: 1, action: 'Story generated', time: '10:30 AM', words: 287 },
    { id: 2, action: 'Auto-save completed', time: '10:25 AM', words: 0 },
    { id: 3, action: 'Daily writing started', time: '9:45 AM', words: 0 },
    { id: 4, action: 'Backup created', time: 'Yesterday', words: 12163 }
  ]);

  const progressPercentage = Math.min((stats.wordsToday / stats.dailyGoal) * 100, 100);

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>📊 Writing Dashboard</h2>
        <p>Monitor your novel writing progress and statistics</p>
      </div>

      {/* Key Statistics Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📝</div>
          <div className="stat-content">
            <h3>Total Words</h3>
            <p className="stat-number">{stats.totalWords.toLocaleString()}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <h3>Daily Progress</h3>
            <p className="stat-number">{stats.wordsToday} / {stats.dailyGoal}</p>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${progressPercentage}%` }}
              ></div>
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔥</div>
          <div className="stat-content">
            <h3>Writing Streak</h3>
            <p className="stat-number">{stats.currentStreak} days</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💾</div>
          <div className="stat-content">
            <h3>Last Save</h3>
            <p className="stat-number">{stats.lastSave}</p>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <h3>⚡ Quick Actions</h3>
        <div className="action-buttons">
          <button className="action-btn primary">
            📚 Generate Today's Page
          </button>
          <button className="action-btn secondary">
            📖 View Latest Story
          </button>
          <button className="action-btn secondary">
            💾 Create Backup
          </button>
          <button className="action-btn secondary">
            📊 View Analytics
          </button>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="recent-activity">
        <h3>📈 Recent Activity</h3>
        <div className="activity-list">
          {recentActivity.map(activity => (
            <div key={activity.id} className="activity-item">
              <div className="activity-time">{activity.time}</div>
              <div className="activity-content">
                <span className="activity-action">{activity.action}</span>
                {activity.words > 0 && (
                  <span className="activity-words">({activity.words} words)</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* System Status */}
      <div className="system-status">
        <h3>⚙️ System Status</h3>
        <div className="status-indicators">
          <div className="status-item">
            <span className="status-dot online"></span>
            <span>AI Agent: Active</span>
          </div>
          <div className="status-item">
            <span className="status-dot online"></span>
            <span>Auto-save: Enabled</span>
          </div>
          <div className="status-item">
            <span className="status-dot online"></span>
            <span>News Integration: Connected</span>
          </div>
          <div className="status-item">
            <span className="status-dot warning"></span>
            <span>Weather API: Limited</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
