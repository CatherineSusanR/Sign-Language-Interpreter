'use client';

import { useRef, useState } from 'react';

export default function AudioToSign() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcribedText, setTranscribedText] = useState('');
  const [signDescription, setSignDescription] = useState('');

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type.startsWith('audio/')) {
      setAudioFile(file);
      setTranscribedText('');
      setSignDescription('');
    } else {
      alert('Please select a valid audio file');
    }
  };

  const processAudio = async () => {
    if (!audioFile) return;

    setIsProcessing(true);
    try {
      // Simulate audio transcription using Web Speech API or external service
      // In production, you'd use speech-to-text API (Google Cloud Speech, Whisper, etc.)
      await new Promise((resolve) => setTimeout(resolve, 2000));

      const mockTranscriptions = [
        'Hello, how are you today?',
        'Thank you very much for your help',
        'Good morning, nice to meet you',
        'Can you help me with this project?',
        'I appreciate your kindness and support',
      ];
      const randomTranscription =
        mockTranscriptions[Math.floor(Math.random() * mockTranscriptions.length)];

      setTranscribedText(randomTranscription);

      // Convert transcribed text to sign description
      const signDescriptions: { [key: string]: string } = {
        hello: 'Open hand touching forehead, moving forward',
        thank: 'Hand near chin, moving outward twice',
        good: 'Hand moves from mouth downward to other hand palm up',
        morning: 'One arm represents the sun, other arm moves up',
        help: 'One hand formed like a fist under the other palm',
        appreciate: 'Both hands on chest, moving outward in grateful motion',
        kindness: 'Fingers tap chest over heart repeatedly',
      };

      let description = 'Sign sequence: ';
      const words = randomTranscription
        .toLowerCase()
        .split(' ')
        .filter((w) => w.length > 2);
      description += words
        .map((word) => signDescriptions[word] || `Finger-spell "${word}"`)
        .join(' → ');

      setSignDescription(description);
    } catch (error) {
      console.error('Error processing audio:', error);
      alert('Error processing audio file');
    } finally {
      setIsProcessing(false);
    }
  };

  const clearFile = () => {
    setAudioFile(null);
    setTranscribedText('');
    setSignDescription('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="space-y-6">
      <div className="space-y-3">
        <label className="block text-sm font-medium">Upload Audio File</label>
        <input
          ref={fileInputRef}
          type="file"
          accept="audio/*"
          onChange={handleFileSelect}
          className="hidden"
        />
        <button
          onClick={() => fileInputRef.current?.click()}
          className="w-full px-6 py-8 border-2 border-dashed border-border rounded-lg hover:border-accent hover:bg-secondary/30 transition-colors cursor-pointer"
        >
          <div className="text-center">
            <p className="text-2xl mb-2">🎤</p>
            <p className="font-medium">Click to select audio file</p>
            <p className="text-sm text-muted-foreground mt-1">or drag and drop</p>
          </div>
        </button>
      </div>

      {audioFile && (
        <div className="bg-secondary/50 rounded-lg p-4 space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Selected file:</p>
              <p className="font-medium">{audioFile.name}</p>
              <p className="text-xs text-muted-foreground mt-1">{(audioFile.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
            <button
              onClick={clearFile}
              className="px-3 py-1 bg-destructive/20 text-destructive rounded hover:bg-destructive/30 text-sm"
            >
              Remove
            </button>
          </div>

          <audio controls className="w-full rounded">
            <source src={URL.createObjectURL(audioFile)} type={audioFile.type} />
            Your browser does not support the audio element.
          </audio>

          <button
            onClick={processAudio}
            disabled={isProcessing}
            className="w-full px-6 py-3 bg-accent text-accent-foreground rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {isProcessing ? 'Converting Audio...' : 'Convert Audio to Sign Language'}
          </button>
        </div>
      )}

      {transcribedText && (
        <div className="bg-secondary/50 rounded-lg p-6 space-y-4">
          <div>
            <p className="text-sm text-muted-foreground mb-2">Transcribed Text:</p>
            <p className="text-lg font-semibold">{transcribedText}</p>
          </div>

          {signDescription && (
            <div className="border-t border-border pt-4">
              <p className="text-sm text-muted-foreground mb-2">Sign Language Guide:</p>
              <p className="text-base leading-relaxed">{signDescription}</p>
            </div>
          )}

          <div className="bg-secondary/30 rounded p-3 text-sm text-muted-foreground italic">
            💡 Learn the signs step by step to understand the full message.
          </div>
        </div>
      )}

      {!audioFile && (
        <div className="bg-secondary/20 rounded-lg p-4 text-sm text-muted-foreground">
          <p>Supported formats: MP3, WAV, OGG, M4A, and other common audio formats</p>
        </div>
      )}
    </div>
  );
}
