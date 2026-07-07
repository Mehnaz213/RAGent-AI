'use client';

// Import the React type used for the chat reference
import { RefObject } from 'react';

// Import a utility to display timestamps like "2 minutes ago"
import { formatDistanceToNow } from 'date-fns';

// Import icons used in the chat interface
import { Bot, User, FileText, Clock, Brain } from 'lucide-react';

// Define the structure of one chat message
interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
    sources?: string[];
}

// Define the data this component receives from page.tsx
interface ChatAreaProps {
    messages: Message[];
    isLoading: boolean;
    chatEndRef: RefObject<HTMLDivElement>;
}

// Create the ChatArea component
export default function ChatArea({
    messages,
    isLoading,
    chatEndRef,
}: ChatAreaProps) {
    return (
        // Main chat container
        <div className="flex-1 flex flex-col overflow-hidden">

            {/* ================= Header ================= */}

            {/* Display the application title and description */}
            <div className="glass-elevated border-b border-white/10 px-8 py-6">
                <h2 className="text-2xl font-semibold gradient-text mb-2">
                    Enterprise AI Agent
                </h2>

                <p className="text-sm text-muted-foreground">
                    Ask questions across your organization's knowledge base using
                    Retrieval-Augmented Generation, semantic search,
                    cross-encoder reranking, and conversational memory.
                </p>
            </div>

            {/* ================= Chat Messages ================= */}

            <div className="flex-1 overflow-y-auto px-8 py-6 space-y-6">

                {/* If there are no messages, show the welcome screen */}
                {messages.length === 0 ? (

                    <div className="h-full flex items-center justify-center">

                        <div className="text-center max-w-md">

                            {/* Welcome Icon */}
                            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500/20 to-cyan-500/20 border border-blue-500/30 flex items-center justify-center mx-auto mb-4">
                                <Brain className="w-8 h-8 text-cyan-400" />
                            </div>

                            {/* Welcome Title */}
                            <h3 className="text-xl font-semibold mb-2">
                                Enterprise AI Agent
                            </h3>

                            {/* Welcome Description */}
                            <p className="text-muted-foreground text-sm">
                                Ask questions across your organization's knowledge base
                                using Retrieval-Augmented Generation, semantic search,
                                cross-encoder reranking, and conversational memory.
                            </p>

                        </div>

                    </div>

                ) : (

                    <>
                        {/* Loop through every message and display it */}
                        {messages.map((message) => (

                            <div
                                key={message.id}
                                className={`flex gap-4 animate-in fade-in slide-in-from-bottom-2 duration-500 ${message.role === 'user'
                                    ? 'justify-end'
                                    : 'justify-start'
                                    }`}
                            >

                                {/* Show AI icon for assistant messages */}
                                {message.role === 'assistant' && (

                                    <div className="flex-shrink-0">

                                        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">

                                            <Bot className="w-5 h-5 text-white" />

                                        </div>

                                    </div>

                                )}

                                {/* Chat Bubble */}
                                <div
                                    className={`flex flex-col gap-2 max-w-2xl ${message.role === 'user'
                                        ? 'items-end'
                                        : 'items-start'
                                        }`}
                                >

                                    {/* Display the message text */}
                                    <div
                                        className={`rounded-2xl px-4 py-3 smooth-transition ${message.role === 'user'
                                            ? 'glass-elevated border-blue-500/20 text-foreground'
                                            : 'glass border-white/10 text-foreground'
                                            }`}
                                    >
                                        <p className="text-sm leading-relaxed">
                                            {message.content}
                                        </p>
                                    </div>

                                    {/* Show source documents only for AI responses */}
                                    {message.role === 'assistant' &&
                                        message.sources &&
                                        message.sources.length > 0 && (

                                            <div className="flex items-start gap-2 text-xs text-muted-foreground mt-1">

                                                <FileText className="w-4 h-4 flex-shrink-0 mt-0.5" />

                                                <div>

                                                    <p className="font-medium mb-1">
                                                        Sources:
                                                    </p>

                                                    <div className="flex flex-wrap gap-2">

                                                        {/* Display every retrieved source */}
                                                        {message.sources.map((source, idx) => (

                                                            <span
                                                                key={idx}
                                                                className="glass rounded px-2 py-1 border-white/10 text-xs"
                                                            >
                                                                {source}
                                                            </span>

                                                        ))}

                                                    </div>

                                                </div>

                                            </div>

                                        )}

                                    {/* Display message timestamp */}
                                    <div className="flex items-center gap-1 text-xs text-muted-foreground">

                                        <Clock className="w-3 h-3" />

                                        <span>
                                            {formatDistanceToNow(
                                                message.timestamp,
                                                { addSuffix: true }
                                            )}
                                        </span>

                                    </div>

                                </div>

                                {/* Show User icon for user messages */}
                                {message.role === 'user' && (

                                    <div className="flex-shrink-0">

                                        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-slate-400 to-slate-500 flex items-center justify-center">

                                            <User className="w-5 h-5 text-white" />

                                        </div>

                                    </div>

                                )}

                            </div>

                        ))}

                        {/* Show typing animation while waiting for AI */}
                        {isLoading && (

                            <div className="flex gap-4 animate-in fade-in slide-in-from-bottom-2 duration-500">

                                {/* AI Icon */}
                                <div className="flex-shrink-0">

                                    <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">

                                        <Bot className="w-5 h-5 text-white" />

                                    </div>

                                </div>

                                {/* Typing Indicator */}
                                <div className="flex items-center gap-2 glass rounded-2xl px-4 py-3 border-white/10">

                                    <div className="flex gap-1">

                                        <div className="w-2 h-2 rounded-full bg-cyan-400 typing-indicator" />

                                        <div
                                            className="w-2 h-2 rounded-full bg-cyan-400 typing-indicator"
                                            style={{ animationDelay: '0.2s' }}
                                        />

                                        <div
                                            className="w-2 h-2 rounded-full bg-cyan-400 typing-indicator"
                                            style={{ animationDelay: '0.4s' }}
                                        />

                                    </div>

                                    <span className="text-xs text-muted-foreground ml-1">
                                        Thinking...
                                    </span>

                                </div>

                            </div>

                        )}

                        {/* Invisible element used for automatic scrolling */}
                        <div ref={chatEndRef} />

                    </>

                )}

            </div>

        </div>
    );
}