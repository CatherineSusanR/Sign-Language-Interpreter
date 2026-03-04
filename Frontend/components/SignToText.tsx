'use client';

import { useRef, useState } from 'react';
import VideoPreview from './VideoPreview';

export default function SignToText() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [detectedText, setDetectedText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setIsRecording(true);
      }
    } catch (error) {
      console.error('Camera access denied:', error);
      alert('Camera access denied. Please enable camera permissions.');
    }
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const tracks = (videoRef.current.srcObject as MediaStream).getTracks();
      tracks.forEach((track) => track.stop());
      setIsRecording(false);
    }
  };

  const captureFrame = async () => {
    if (!videoRef.current) return;

    setIsLoading(true);
    try {
      // Simulate sign language detection
      // In production, you'd send the frame to a ML model (MediaPipe Hands, etc.)
      await new Promise((resolve) => setTimeout(resolve, 1500));

      const mockSignDetections = [
        'Hello',
        'Thank you',
        'Good morning',
        'How are you',
        'Nice to meet you',
      ];
      const randomText = mockSignDetections[Math.floor(Math.random() * mockSignDetections.length)];
      setDetectedText(randomText);
    } catch (error) {
      console.error('Error detecting sign:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(detectedText);
    alert('Text copied to clipboard!');
  };

  return (
    <div className="space-y-6">
      <div className="bg-secondary/30 rounded-lg p-1">
        {isRecording ? (
          <VideoPreview ref={videoRef} isRecording={isRecording} />
        ) : (
          <div className="w-full aspect-video bg-secondary rounded-lg flex items-center justify-center">
            <p className="text-muted-foreground">Camera will appear here</p>
          </div>
        )}
      </div>

      <div className="flex gap-3 flex-wrap">
        {!isRecording ? (
          <button
            onClick={startCamera}
            className="flex-1 min-w-fit px-6 py-3 bg-accent text-accent-foreground rounded-lg font-medium hover:opacity-90 transition-opacity"
          >
            Start Camera
          </button>
        ) : (
          <>
            <button
              onClick={captureFrame}
              disabled={isLoading}
              className="flex-1 min-w-fit px-6 py-3 bg-accent text-accent-foreground rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {isLoading ? 'Detecting...' : 'Detect Sign'}
            </button>
            <button
              onClick={stopCamera}
              className="flex-1 min-w-fit px-6 py-3 bg-destructive/20 text-destructive rounded-lg font-medium hover:bg-destructive/30 transition-colors"
            >
              Stop Camera
            </button>
          </>
        )}
      </div>

      {detectedText && (
        <div className="bg-secondary/50 rounded-lg p-4 space-y-3">
          <p className="text-sm text-muted-foreground">Detected Text:</p>
          <p className="text-2xl font-semibold">{detectedText}</p>
          <button
            onClick={copyToClipboard}
            className="w-full px-4 py-2 bg-primary/20 text-primary rounded-lg font-medium hover:bg-primary/30 transition-colors"
          >
            Copy Text
          </button>
        </div>
      )}
    </div>
  );
}
