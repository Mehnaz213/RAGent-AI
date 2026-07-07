// Mark this file as a Client Component so it can use React Hooks and browser features
'use client';
// Import React Hooks
import { useState, useRef, useEffect } from 'react';
import Sidebar from '@/components/sidebar';
import ChatArea from '@/components/chat-area';
import ChatInput from '@/components/chat-input';
import UploadStatus from '@/components/upload-status';

// Export the main page component
export default function Page() {
  // Store all chat messages
  const [messages, setMessages] = useState<
    Array<{
      id: string;
      role: 'user' | 'assistant';
      content: string;
      timestamp: Date;
      sources?: string[];
    }>
  >([]);

  // Store whether the AI is generating a response
  const [isLoading, setIsLoading] = useState(false);

  // Store the current PDF upload status
  const [uploadStatus, setUploadStatus] = useState<
    'idle' | 'processing' | 'success' | 'error'
  >('idle');

  // Store the uploaded PDF filename
  const [uploadFileName, setUploadFileName] = useState<string>('');

  // Store the number of chunks created after PDF processing
  const [uploadChunkCount, setUploadChunkCount] = useState<number>(0);

  // Store upload error messages
  const [uploadError, setUploadError] = useState<string>('');

  // Create a reference to the bottom of the chat
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Function to automatically scroll to the latest message
  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({
      behavior: 'smooth',
    });
  };

  // Automatically scroll whenever messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Function to handle sending messages
  const handleSendMessage = async (message: string) => {

    // Ignore empty messages
    if (!message.trim()) return;

    // Create a new user message
    const userMessage = {
      id: Date.now().toString(),
      role: 'user' as const,
      content: message,
      timestamp: new Date(),
    };

    // Add the user message to chat
    setMessages(prev => [...prev, userMessage]);

    // Show loading animation
    setIsLoading(true);

    try {
      // Send the question to FastAPI
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            question: message
          })
        }
      );
      // Check if the request was successful
      if (!response.ok) {
        throw new Error("Failed to get AI response");
      }
      // Convert JSON response to JavaScript object
      const data = await response.json();

      // Create assistant message
      const aiMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant" as const,
        content: data.answer,
        timestamp: new Date()
      };

      // Display AI response
      setMessages(prev => [...prev, aiMessage]);
    }
    catch (error) {
      console.error("Fetch Error:", error);
      if (error instanceof Error) {
        alert(error.message);
      }
    }
    finally {
      setIsLoading(false);
    }
  };
  // Function to clear all chat messages
  const handleClearChat = () => {
    setMessages([]);
  };

  // Function to upload a PDF
  const handleUploadPDF = async (file: File) => {
    console.log("Upload function called");

    // Show processing status
    setUploadStatus('processing');

    // Store uploaded filename
    setUploadFileName(file.name);

    // Clear previous errors
    setUploadError('');

    try {

      // Create form data
      const formData = new FormData();
      // Add PDF file
      formData.append("pdf", file);
      // Send PDF to FastAPI
      const response = await fetch(
        "http://localhost:8000/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      // Convert response to JSON
      const data = await response.json();
      // Show uploaded filename
      setUploadFileName(data.filename);
      // Temporary chunk count
      setUploadChunkCount(1);
      // Show success
      setUploadStatus('success');

      // Hide notification after 4 seconds
      setTimeout(() => {
        setUploadStatus('idle');
      }, 4000);

    } catch (error) {

      // Store error message
      setUploadError(
        error instanceof Error
          ? error.message
          : 'Failed to process PDF'
      );

      // Show error status
      setUploadStatus('error');

      // Hide notification after 4 seconds
      setTimeout(() => {
        setUploadStatus('idle');
      }, 4000);
    }
  };

  // Return the complete page UI
  return (

    // Main application container
    <div className="flex h-screen bg-background dark">

      {/* Sidebar */}
      <Sidebar
        onClearChat={handleClearChat}
        onUploadPDF={handleUploadPDF}
      />

      {/* Chat Section */}
      <div className="flex flex-1 flex-col overflow-hidden">

        {/* Display chat messages */}
        <ChatArea
          messages={messages}
          isLoading={isLoading}
          chatEndRef={chatEndRef}
        />

        {/* Message input */}
        <ChatInput
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
        />

      </div>

      {/* Upload notification */}
      <UploadStatus
        status={uploadStatus}
        fileName={uploadFileName}
        chunkCount={uploadChunkCount}
        error={uploadError}
      />

    </div>
  );
}