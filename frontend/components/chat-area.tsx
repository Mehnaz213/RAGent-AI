'use client';

import { useState } from "react";
import {
    Brain,
    User,
    FileText,
    Copy,
    Check
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Message {
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
}

interface ChatAreaProps {
    messages: Message[];
    isLoading: boolean;
    chatEndRef: React.RefObject<HTMLDivElement | null>;
    onSuggestionClick: (question: string) => void;
}

export default function ChatArea({
    messages,
    isLoading,
    chatEndRef,
    onSuggestionClick,
}: ChatAreaProps) {

    const [copiedMessage, setCopiedMessage] =
        useState<string | null>(null);

    const copyMessage = async (
        id: string,
        text: string
    ) => {

        await navigator.clipboard.writeText(text);

        setCopiedMessage(id);

        setTimeout(() => {
            setCopiedMessage(null);
        }, 2000);

    };

    return (
        <div className="flex-1 flex flex-col overflow-hidden">

            <div className="flex-1 overflow-y-auto px-8 py-10 space-y-6">

                {messages.length === 0 ? (

                    <div className="h-full flex items-center justify-center">

                        <div className="text-center max-w-lg">

                            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-sky-400 to-cyan-400 flex items-center justify-center mx-auto mb-4">
                                <Brain className="w-8 h-8 text-white" />
                            </div>

                            <h3 className="text-3xl font-bold gradient-text mb-3">
                                RAGent AI
                            </h3>

                            <p className="text-muted-foreground">
                                Ask questions about your organization's knowledge base.
                            </p>

                            <p className="text-xs text-muted-foreground mt-3">
                                Powered by Retrieval-Augmented Generation (RAG)
                            </p>

                            <div className="mt-8 text-left glass rounded-xl p-5 border border-border">

                                <div className="grid gap-2">

                                    {[
                                        "Summarize the employee handbook",
                                        "Explain the leave policy",
                                        "Explain the dress code",
                                        "What are the working hours?"
                                    ].map((question) => (

                                        <button
                                            key={question}
                                            onClick={() => onSuggestionClick(question)}
                                            className="text-left rounded-lg border border-border px-3 py-2 hover:border-cyan-400 hover:bg-cyan-500/10 transition"
                                        >
                                            {question}
                                        </button>

                                    ))}

                                </div>

                            </div>

                        </div>

                    </div>

                ) : (

                    <>

                        {messages.map((message) => (

                            <div
                                key={message.id}
                                className={`flex gap-4 ${message.role === "user"
                                    ? "justify-end"
                                    : "justify-start"
                                    }`}
                            >

                                {/* Assistant Avatar */}
                                {message.role === "assistant" && (

                                    <div className="flex-shrink-0">

                                        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">

                                            <Brain className="w-5 h-5 text-white" />

                                        </div>

                                    </div>

                                )}

                                {/* Message */}

                                <div
                                    className={`flex flex-col gap-2 max-w-2xl ${message.role === "user"
                                        ? "items-end"
                                        : "items-start"
                                        }`}
                                >
                                    {message.role === "assistant" &&
                                        message.agent &&
                                        message.agent.steps.length > 0 && (

                                            <div className="w-full rounded-2xl border border-cyan-500/30 bg-cyan-500/5 p-4 mb-2">

                                                <div className="flex items-center gap-2 mb-3">

                                                    <Brain className="w-5 h-5 text-cyan-400" />

                                                    <p className="font-semibold text-cyan-400">

                                                        Agent Execution

                                                    </p>

                                                </div>

                                                <div className="space-y-2">

                                                    {message.agent.steps.map((step, index) => (

                                                        <div
                                                            key={index}
                                                            className="flex items-center gap-2 text-sm"
                                                        >

                                                            <span className="text-green-400">

                                                                ✓

                                                            </span>

                                                            <span>

                                                                {step}

                                                            </span>

                                                        </div>

                                                    ))}

                                                </div>

                                            </div>

                                        )}
                                    <div
                                        className={`rounded-2xl px-4 py-3 ${message.role === "user"
                                            ? "bg-primary text-white"
                                            : "glass border border-border text-foreground"
                                            }`}
                                    >

                                        <div className="prose prose-invert max-w-none prose-headings:text-white prose-p:text-gray-200 prose-strong:text-cyan-300 prose-li:text-gray-200 prose-code:text-cyan-300">

                                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                                {message.content}
                                            </ReactMarkdown>

                                        </div>

                                    </div>

                                    {/* Sources */}

                                    {message.role === "assistant" &&
                                        message.sources &&
                                        message.sources.length > 0 && (

                                            <div className="flex items-start gap-2 text-xs text-muted-foreground">

                                                <FileText className="w-4 h-4 mt-0.5" />

                                                <div>

                                                    <p className="font-medium mb-1">
                                                        Sources:
                                                    </p>

                                                    <div className="flex flex-wrap gap-2">

                                                        {(() => {

                                                            const groupedSources: Record<string, number[]> = {};

                                                            message.sources.forEach((item) => {

                                                                if (!groupedSources[item.source]) {
                                                                    groupedSources[item.source] = [];
                                                                }

                                                                groupedSources[item.source].push(item.page);

                                                            });

                                                            return Object.entries(groupedSources).map(([file, pages]) => {

                                                                const displayName = file
                                                                    .replace(".pdf", "")
                                                                    .replaceAll("_", " ");

                                                                const url =
                                                                    `/viewer?file=${encodeURIComponent(file)}&page=${pages[0]}`;

                                                                return (

                                                                    <button
                                                                        key={file}
                                                                        onClick={() => window.open(url, "_blank")}
                                                                        className="glass rounded-lg px-3 py-2 border border-border hover:border-cyan-400 hover:bg-cyan-500/10 transition text-left"
                                                                    >

                                                                        <p className="font-medium text-white">
                                                                            📄 {displayName}
                                                                        </p>

                                                                        <p className="text-xs text-muted-foreground">
                                                                            Pages: {pages.join(", ")}
                                                                        </p>

                                                                    </button>

                                                                );

                                                            });

                                                        })()}

                                                    </div>

                                                </div>

                                            </div>

                                        )}

                                    {/* Copy */}
                                    <div className="flex gap-4">
                                        {message.role === "assistant" && (

                                            <button
                                                onClick={() =>
                                                    copyMessage(
                                                        message.id,
                                                        message.content
                                                    )
                                                }
                                                className="flex items-center gap-2 text-xs text-cyan-400 hover:text-cyan-300 transition"
                                            >

                                                {copiedMessage === message.id ? (

                                                    <>
                                                        <Check className="w-4 h-4" />
                                                        Copied
                                                    </>

                                                ) : (

                                                    <>
                                                        <Copy className="w-4 h-4" />
                                                        Copy
                                                    </>

                                                )}

                                            </button>

                                        )}
                                    </div>
                                </div>
                                {/* User Avatar */}

                                {message.role === "user" && (

                                    <div className="flex-shrink-0">

                                        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">

                                            <User className="w-5 h-5 text-white" />

                                        </div>

                                    </div>

                                )}

                            </div>

                        ))}

                        {isLoading && (

                            <div className="flex gap-4">

                                <div className="flex-shrink-0">

                                    <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-sky-500 to-cyan-500 flex items-center justify-center">

                                        <Brain className="w-5 h-5 text-white" />

                                    </div>

                                </div>

                                <div className="glass rounded-2xl px-4 py-3 border border-border flex items-center gap-2">

                                    <div className="flex gap-1">

                                        <div className="w-2 h-2 rounded-full bg-cyan-400 typing-indicator" />

                                        <div
                                            className="w-2 h-2 rounded-full bg-cyan-400 typing-indicator"
                                            style={{ animationDelay: "0.2s" }}
                                        />

                                        <div
                                            className="w-2 h-2 rounded-full bg-cyan-400 typing-indicator"
                                            style={{ animationDelay: "0.4s" }}
                                        />

                                    </div>

                                    <div className="flex flex-col">

                                        <span className="text-sm font-medium">
                                            🤖 Agent is working...
                                        </span>

                                        <span className="text-xs text-muted-foreground">
                                            Planning and executing your request.
                                        </span>

                                    </div>

                                </div>

                            </div>

                        )}

                        <div ref={chatEndRef} />

                    </>

                )}

            </div>

        </div>
    );
}