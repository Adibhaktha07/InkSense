import React, { useState } from 'react';
import VideoStream from './components/VideoStream';

function App() {
  const [color, setColor] = useState("#ff00ff");

  const clearCanvas = () => {
    fetch("http://localhost:5000/clear", { method: "POST" })
      .then(() => alert("Canvas cleared!"));
  };

  const changeColor = (e) => {
    const selected = e.target.value;
    setColor(selected);
    fetch("http://localhost:5000/color", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ color: selected })
    });
  };

  return (
    <div style={appStyle}>
      <h1 style={{ color: '#fff' }}>InkSense - AI Gesture Drawing</h1>

      <div style={videoContainer}>
        <VideoStream />
      </div>

      <div style={controls}>
        <input
          type="color"
          value={color}
          onChange={changeColor}
          style={{ ...buttonStyle, padding: '5px', width: '60px' }}
          title="Select brush color"
        />
        <button onClick={clearCanvas} style={buttonStyle}>Clear Canvas</button>
      </div>
    </div>
  );
}

const appStyle = {
  height: '100vh',
  margin: 0,
  padding: 0,
  background: 'linear-gradient(to right, #1e3c72, #2a5298)',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center'
};

const videoContainer = {
  position: 'relative',
  width: '90%',
  maxWidth: '960px',
  border: '5px solid white',
  borderRadius: '10px',
  overflow: 'hidden',
};

const controls = {
  marginTop: '20px',
  display: 'flex',
  gap: '15px',
  alignItems: 'center',
};

const buttonStyle = {
  padding: '12px 20px',
  fontSize: '16px',
  fontWeight: 'bold',
  borderRadius: '6px',
  border: 'none',
  background: '#fff',
  color: '#333',
  cursor: 'pointer',
};

export default App;
