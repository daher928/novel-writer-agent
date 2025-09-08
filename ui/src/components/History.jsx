import React from 'react';

const History = () => {
  // Placeholder data for previous daily generations
  const historyData = [
    {
      id: 1,
      date: '2024-03-15',
      preview: 'Chapter 1: The mysterious fog rolled through the ancient forest, carrying whispers of long-forgotten secrets...',
      wordCount: 1250,
      title: 'The Enchanted Forest - Chapter 1'
    },
    {
      id: 2,
      date: '2024-03-14',
      preview: 'In the bustling streets of Victorian London, Detective Morrison discovered a clue that would change everything...',
      wordCount: 980,
      title: 'Victorian Mystery - Opening Scene'
    },
    {
      id: 3,
      date: '2024-03-13',
      preview: 'The spaceship trembled as it entered the atmosphere of the unknown planet, its crew preparing for first contact...',
      wordCount: 1400,
      title: 'First Contact - Landing Sequence'
    },
    {
      id: 4,
      date: '2024-03-12',
      preview: 'Sarah\'s hands shook as she opened the letter that had been waiting for her for twenty years...',
      wordCount: 850,
      title: 'Long Lost Letters - Part 1'
    },
    {
      id: 5,
      date: '2024-03-11',
      preview: 'The dragon\'s eyes gleamed in the candlelight as the young knight approached the ancient lair...',
      wordCount: 1150,
      title: 'Dragon Knight - Final Battle'
    }
  ];

  const handleRestore = (id) => {
    // TODO: Implement restore functionality
    console.log(`Restoring generation with id: ${id}`);
  };

  const handleDownload = (id, title) => {
    // TODO: Implement download functionality
    console.log(`Downloading: ${title} (id: ${id})`);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="history-container">
      <div className="history-header">
        <h1>Generation History</h1>
        <p>View and manage your previous daily novel generations</p>
      </div>

      <div className="history-timeline">
        {historyData.map((item) => (
          <div key={item.id} className="history-item">
            <div className="history-item-header">
              <div className="history-date">
                <div className="date-badge">
                  {formatDate(item.date)}
                </div>
                <div className="word-count">
                  {item.wordCount} words
                </div>
              </div>
              <div className="history-actions">
                <button 
                  className="btn btn-secondary"
                  onClick={() => handleRestore(item.id)}
                  title="Restore this generation to editor"
                >
                  Restore
                </button>
                <button 
                  className="btn btn-primary"
                  onClick={() => handleDownload(item.id, item.title)}
                  title="Download as file"
                >
                  Download
                </button>
              </div>
            </div>
            
            <div className="history-content">
              <h3 className="history-title">{item.title}</h3>
              <div className="history-preview">
                {item.preview}
                {item.preview.length > 100 && (
                  <span className="preview-ellipsis">...</span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {historyData.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">📚</div>
          <h3>No Generation History</h3>
          <p>Your daily novel generations will appear here once you start creating.</p>
        </div>
      )}

      <style jsx>{`
        .history-container {
          max-width: 800px;
          margin: 0 auto;
          padding: 2rem;
        }

        .history-header {
          text-align: center;
          margin-bottom: 2rem;
        }

        .history-header h1 {
          color: #2c3e50;
          margin-bottom: 0.5rem;
        }

        .history-header p {
          color: #7f8c8d;
          font-size: 1.1rem;
        }

        .history-timeline {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .history-item {
          background: #ffffff;
          border: 1px solid #e1e8ed;
          border-radius: 12px;
          padding: 1.5rem;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .history-item:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .history-item-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 1rem;
        }

        .history-date {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }

        .date-badge {
          background: #3498db;
          color: white;
          padding: 0.25rem 0.75rem;
          border-radius: 20px;
          font-size: 0.9rem;
          font-weight: 500;
          width: fit-content;
        }

        .word-count {
          font-size: 0.8rem;
          color: #7f8c8d;
          margin-left: 0.75rem;
        }

        .history-actions {
          display: flex;
          gap: 0.5rem;
        }

        .btn {
          padding: 0.5rem 1rem;
          border: none;
          border-radius: 6px;
          font-size: 0.9rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .btn-secondary {
          background: #95a5a6;
          color: white;
        }

        .btn-secondary:hover {
          background: #7f8c8d;
        }

        .btn-primary {
          background: #3498db;
          color: white;
        }

        .btn-primary:hover {
          background: #2980b9;
        }

        .history-title {
          color: #2c3e50;
          margin-bottom: 0.75rem;
          font-size: 1.2rem;
        }

        .history-preview {
          color: #34495e;
          line-height: 1.6;
          font-size: 1rem;
        }

        .preview-ellipsis {
          color: #95a5a6;
          font-weight: bold;
        }

        .empty-state {
          text-align: center;
          padding: 3rem 1rem;
          color: #7f8c8d;
        }

        .empty-icon {
          font-size: 3rem;
          margin-bottom: 1rem;
        }

        .empty-state h3 {
          color: #2c3e50;
          margin-bottom: 1rem;
        }

        @media (max-width: 768px) {
          .history-container {
            padding: 1rem;
          }

          .history-item-header {
            flex-direction: column;
            gap: 1rem;
          }

          .history-actions {
            align-self: flex-end;
          }

          .btn {
            font-size: 0.8rem;
            padding: 0.4rem 0.8rem;
          }
        }
      `}</style>
    </div>
  );
};

export default History;
