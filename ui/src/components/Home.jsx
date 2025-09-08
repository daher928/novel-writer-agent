import React, { useState } from 'react';
import './Home.css';

const Home = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [storyText, setStoryText] = useState(
    "The morning sun cast long shadows across the cobblestone streets of the old town. Sarah pulled her coat tighter against the autumn chill as she hurried toward the mysterious letter that had arrived at dawn. Little did she know, this single piece of parchment would change everything she thought she knew about her quiet life in Millbrook..."
  );

  // Dummy data for inspiration sources
  const inspirationData = {
    mood: {
      current: 'Mysterious',
      options: ['Adventurous', 'Romantic', 'Mysterious', 'Dramatic', 'Whimsical']
    },
    news: [
      { title: 'Ancient Library Discovered', relevance: 'Historical Fiction' },
      { title: 'Tech Breakthrough in AI', relevance: 'Sci-Fi' },
      { title: 'Small Town Festival', relevance: 'Contemporary' }
    ]
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    // Simulate generation process
    setTimeout(() => {
      setStoryText(
        "The clock tower chimed midnight as Elena discovered the hidden passage behind the bookshelf. The dusty corridor stretched into darkness, lit only by flickering torches that seemed to ignite themselves as she passed. Each step echoed with whispers of forgotten stories, and she realized she had stumbled upon something far more extraordinary than she had ever imagined..."
      );
      setIsGenerating(false);
    }, 3000);
  };

  const handleReroll = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setStoryText(
        "Detective Martinez stared at the cryptic message scrawled on the warehouse wall. Three cases, three different cities, but the same strange symbol appeared at each crime scene. As rain began to fall, washing away the chalk dust, she knew this wasn't just another routine investigation—someone was playing a very dangerous game..."
      );
      setIsGenerating(false);
    }, 2000);
  };

  const handleSave = () => {
    // Simulate save operation
    console.log('Story saved:', storyText);
    alert('Story saved successfully!');
  };

  return (
    <div className="home-container">
      <div className="home-header">
        <h1>Today's Generation</h1>
        <div className="date-display">
          {new Date().toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          })}
        </div>
      </div>

      <div className="home-content">
        {/* Today's Generation Area */}
        <div className="generation-area">
          <div className="story-display">
            {isGenerating ? (
              <div className="generating-placeholder">
                <div className="writing-spinner">
                  <div className="spinner-text">Crafting your story</div>
                  <div className="spinner-dots">
                    <span>.</span>
                    <span>.</span>
                    <span>.</span>
                  </div>
                </div>
              </div>
            ) : (
              <div className="story-text">
                {storyText}
              </div>
            )}
          </div>
        </div>

        {/* Sidebar with Inspiration and Controls */}
        <div className="sidebar">
          {/* Inspiration Sources Panel */}
          <div className="inspiration-panel">
            <h3>Inspiration Sources</h3>
            
            {/* Mood Section */}
            <div className="mood-section">
              <h4>Current Mood</h4>
              <div className="current-mood">{inspirationData.mood.current}</div>
              <div className="mood-options">
                {inspirationData.mood.options.map((mood, index) => (
                  <button 
                    key={index} 
                    className={`mood-option ${mood === inspirationData.mood.current ? 'active' : ''}`}
                  >
                    {mood}
                  </button>
                ))}
              </div>
            </div>

            {/* News Section */}
            <div className="news-section">
              <h4>Trending News</h4>
              <div className="news-items">
                {inspirationData.news.map((item, index) => (
                  <div key={index} className="news-item">
                    <div className="news-title">{item.title}</div>
                    <div className="news-relevance">{item.relevance}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Writing Controls */}
          <div className="writing-controls">
            <h3>Writing Controls</h3>
            <div className="control-buttons">
              <button 
                className="control-btn generate-btn" 
                onClick={handleGenerate}
                disabled={isGenerating}
              >
                {isGenerating ? 'Generating...' : 'Generate'}
              </button>
              <button 
                className="control-btn reroll-btn" 
                onClick={handleReroll}
                disabled={isGenerating}
              >
                Reroll
              </button>
              <button 
                className="control-btn save-btn" 
                onClick={handleSave}
                disabled={isGenerating}
              >
                Save
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
