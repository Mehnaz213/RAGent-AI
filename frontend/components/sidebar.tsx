// Run this component in the user's browser because it uses browser events
'use client';

// Import icons from the Lucide React icon library
import { Upload, Trash2, Brain, CheckCircle2 } from 'lucide-react';

import { useRef } from "react";

// Import the reusable Button component
import { Button } from '@/components/ui/button';

// Define the data (props) that this component expects from its parent
interface SidebarProps {
    // Function to clear the chat
    onClearChat: () => void;

    // Optional function to upload a PDF
    onUploadPDF?: (file: File) => void;
}

// Create and export the Sidebar component
export default function Sidebar({
    // Receive functions from page.tsx
    onClearChat,
    onUploadPDF,
}: SidebarProps) {
    // Reference to the hidden file input
    const fileInputRef = useRef<HTMLInputElement>(null);
    return (
        // Main Sidebar Container
        <div className="glass-elevated w-80 border-r border-white/10 flex flex-col">

            {/* ================= Header ================= */}
            <div className="p-6 border-b border-white/10">

                {/* Logo + Title */}
                <div className="flex items-center gap-3 mb-2">

                    {/* Logo Background */}
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-400 to-cyan-400 flex items-center justify-center">

                        {/* Brain Icon */}
                        <Brain className="w-6 h-6 text-background" />

                    </div>

                    {/* App Name */}
                    <h1 className="text-lg font-semibold gradient-text">
                        RAGent AI
                    </h1>

                </div>

                {/* Subtitle */}
                <p className="text-xs text-muted-foreground">
                    Enterprise AI Agent for Retrieval-Augmented Generation
                </p>

            </div>

            {/* ================= Main Actions ================= */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">

                {/* ---------- Upload PDF ---------- */}

                {/* Label is used because the file input is hidden */}
                <label className="cursor-pointer block">

                    <Button
                        type="button"
                        variant="outline"
                        className="w-full justify-start gap-2 glass-hover border-white/10"
                        onClick={() => fileInputRef.current?.click()}
                    >
                        <Upload className="w-4 h-4" />
                        Upload PDF
                    </Button>

                    {/* Hidden File Picker */}
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".pdf"
                        className="hidden"
                        onChange={(e) => {
                            const file = e.target.files?.[0];

                            if (file) {
                                onUploadPDF?.(file);
                            }
                        }}
                    />

                </label>

                {/* ---------- Document Selector ---------- */}
                <div className="mt-6">

                    {/* Section Title */}
                    <p className="text-xs font-semibold text-muted-foreground mb-2 uppercase">
                        Documents
                    </p>

                    {/* Dropdown Container */}
                    <div className="glass rounded-lg p-3">

                        <select className="w-full bg-transparent text-sm text-foreground border-none outline-none cursor-pointer">

                            <option>All Documents</option>
                            <option>document_1.pdf</option>
                            <option>document_2.pdf</option>
                            <option>document_3.pdf</option>

                        </select>

                    </div>

                </div>

                {/* ---------- Clear Chat ---------- */}
                <Button
                    variant="outline"
                    className="w-full justify-start gap-2 glass-hover border-red-500/20 text-red-400 hover:text-red-300 mt-6"
                    onClick={onClearChat}
                >

                    <Trash2 className="w-4 h-4" />

                    Clear Chat

                </Button>

            </div>

            {/* ================= AI Features ================= */}
            <div className="p-4 border-t border-white/10">

                {/* Section Title */}
                <p className="text-xs font-semibold text-muted-foreground mb-3 uppercase">
                    AI Features
                </p>

                {/* Features List */}
                <div className="space-y-2 text-xs">

                    <div className="flex items-center gap-2 text-green-400">
                        <CheckCircle2 className="w-4 h-4" />
                        <span>Retrieval-Augmented Generation</span>
                    </div>

                    <div className="flex items-center gap-2 text-green-400">
                        <CheckCircle2 className="w-4 h-4" />
                        <span>AI Agent Reasoning</span>
                    </div>

                    <div className="flex items-center gap-2 text-green-400">
                        <CheckCircle2 className="w-4 h-4" />
                        <span>Cross Encoder Reranking</span>
                    </div>

                    <div className="flex items-center gap-2 text-green-400">
                        <CheckCircle2 className="w-4 h-4" />
                        <span>Conversation Memory</span>
                    </div>

                    <div className="flex items-center gap-2 text-green-400">
                        <CheckCircle2 className="w-4 h-4" />
                        <span>Multi-Document Search</span>
                    </div>

                    <div className="flex items-center gap-2 text-green-400">
                        <CheckCircle2 className="w-4 h-4" />
                        <span>Source Citations</span>
                    </div>

                </div>

            </div>

        </div>
    );
}