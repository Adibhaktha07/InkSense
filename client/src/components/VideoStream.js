import React from 'react';

const VideoStream = () => {
  return (
    <img
      src="http://localhost:5000/video_feed"
      alt="Live Drawing"
      style={{ width: '100%', height: 'auto' }}
    />
  );
};

export default VideoStream;
