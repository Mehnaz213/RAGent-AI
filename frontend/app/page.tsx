'use client';

import { useState, useRef, useEffect } from 'react';

import { useAuth } from '@/lib/auth-context';

import RoleSelection from '@/components/role-selection';
import Sidebar from '@/components/sidebar';
import ChatArea from '@/components/chat-area';
import ChatInput from '@/components/chat-input';
import UploadStatus from '@/components/upload-status';
import ChatHistoryPage from "@/components/chat-history-page";
import EmployeeSettingsPage from "@/components/employee-settings-page";
import KnowledgeBasePage from "@/components/knowledge-base-page";
import AnalyticsPage from "@/components/analytics-page";

export default function Page() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <RoleSelection />;
  }

  return <MainInterface />;
}

function MainInterface() {
  const [messages, setMessages] = useState<
    Array<{
      id: string;
      role: "user" | "assistant";
      content: string;

      sources?: {
        source: string;
        page: number;
      }[];

      agent?: {
        tools: string[];
        steps: string[];
      };

    }>
  >([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  // Current page shown on the screen
  const [currentPage, setCurrentPage] =
    useState("chat");

  // Used for starting a new conversation
  const [chatKey, setChatKey] =
    useState(0);

  const [isLoading, setIsLoading] = useState(false);

  const [uploadStatus, setUploadStatus] = useState<
    'idle' | 'processing' | 'success' | 'error'
  >('idle');

  const [uploadFileName, setUploadFileName] = useState('');

  const [uploadError, setUploadError] = useState('');

  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: 'smooth',
    });
  }, [messages]);

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user' as const,
      content: message,
    };

    setMessages((prev) => [...prev, userMessage]);

    setIsLoading(true);

    try {
      const token = localStorage.getItem("token");
      console.log("Token:", token);
      let currentConversation = conversationId;

      if (!currentConversation) {

        const conversationResponse = await fetch(
          "http://127.0.0.1:8000/conversation/new",
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!conversationResponse.ok) {
          throw new Error("Failed to create conversation");
        }

        const conversationData =
          await conversationResponse.json();

        currentConversation =
          conversationData.conversation_id;

        setConversationId(currentConversation);
      }
      // Read JWT Token
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",

            Authorization: `Bearer ${token}`,
          },

          body: JSON.stringify({
            question: message,
            conversation_id: currentConversation
          }),
        }
      );

      if (response.status === 401) {

        localStorage.removeItem("token");
        localStorage.removeItem("user");

        window.location.reload();

        return;
      }

      if (!response.ok) {
        throw new Error("Failed to get AI response");
      }

      const data = await response.json();

      const aiMessage = {

        id: (Date.now() + 1).toString(),

        role: "assistant" as const,

        content: data.answer,

        sources: data.sources,

        agent: data.agent

      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setConversationId(null);
  };

  const handleUploadPDF = async (file: File) => {
    setUploadStatus('processing');
    setUploadFileName(file.name);
    setUploadError('');

    try {
      const formData = new FormData();
      formData.append('pdf', file);

      const token = localStorage.getItem("token");
      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",

          headers: {
            Authorization: `Bearer ${token}`,
          },

          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();

      setUploadFileName(data.filename);

      setUploadStatus('success');

      setTimeout(() => {
        setUploadStatus('idle');
      }, 3000);
    } catch (err) {
      setUploadStatus('error');

      setUploadError(
        err instanceof Error ? err.message : 'Upload failed'
      );

      setTimeout(() => {
        setUploadStatus('idle');
      }, 3000);
    }
  };

  return (
    <div className="flex h-screen bg-background dark">
      <Sidebar
        currentPage={currentPage}
        onPageChange={setCurrentPage}
        onClearChat={handleClearChat}
        onUploadPDF={handleUploadPDF}
        onNewChat={() => {
          setMessages([]);
          setConversationId(null);
          setChatKey(prev => prev + 1);
          setCurrentPage("chat");
        }}
      />

      <div className="flex flex-1 flex-col min-h-0">

        {currentPage === "chat" && (
          <>
            <ChatArea
              key={chatKey}
              messages={messages}
              isLoading={isLoading}
              chatEndRef={chatEndRef}
              onSuggestionClick={handleSendMessage}
            />
            <ChatInput
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
            />
          </>
        )}

        {currentPage === "history" && (
          <ChatHistoryPage
            onOpenConversation={async (id) => {

              const token =
                localStorage.getItem("token");

              const response = await fetch(

                `http://127.0.0.1:8000/conversation/${id}`,

                {
                  headers: {
                    Authorization: `Bearer ${token}`
                  }
                }

              );

              if (!response.ok) return;

              const data = await response.json();

              console.log("Backend Messages:", data.messages);

              data.messages.forEach((m: any) => {
                console.log(
                  "Timestamp from backend:",
                  m.timestamp,
                  "Parsed:",
                  "Now:",
                  new Date()
                );
              });
              setConversationId(data.id);
              console.log(data.messages);
              setMessages(
                data.messages.map((m: any, index: number) => ({

                  id: index.toString(),

                  role: m.role,

                  content: m.content,

                  sources: m.sources,

                  agent: m.agent

                }))
              );
              setCurrentPage("chat");

            }}
          />
        )}

        {currentPage === "settings" && (
          <EmployeeSettingsPage />
        )}

        {currentPage === "knowledge-base" && (
          <KnowledgeBasePage />
        )}

        {currentPage === "analytics" && (
          <AnalyticsPage />
        )}



      </div>

      <UploadStatus
        status={uploadStatus}
        fileName={uploadFileName}
        error={uploadError}
      />
    </div>
  );
}