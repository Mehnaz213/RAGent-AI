'use client';
import { useState, useRef } from 'react';
import { Send } from 'lucide-react';
import { Button } from '@/components/ui/button';

// Define the props received from the parent component (page.tsx)
interface ChatInputProps {
    // Function used to send the user's message
    onSendMessage: (message: string) => void;
    // Indicates whether the AI is currently generating a response
    isLoading: boolean;
}

// Create the ChatInput component
export default function ChatInput({
    onSendMessage,
    isLoading,
}: ChatInputProps) {

    // Store the current text typed by the user
    const [input, setInput] = useState('');

    // Reference to the textarea element
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    // Function to send the user's message
    const handleSend = () => {

        // Ignore empty messages
        if (input.trim()) {

            // Send the message to page.tsx
            onSendMessage(input);

            // Clear the textbox
            setInput('');

            // Reset the textarea height
            if (textareaRef.current) {
                textareaRef.current.style.height = 'auto';
            }
        }
    };

    // Runs whenever the user presses a keyboard key
    const handleKeyDown = (
        e: React.KeyboardEvent<HTMLTextAreaElement>
    ) => {

        // Send the message when Enter is pressed
        // Shift + Enter creates a new line
        if (
            e.key === 'Enter' &&
            !e.shiftKey &&
            !e.nativeEvent.isComposing
        ) {

            // Stop the browser from inserting a new line
            e.preventDefault();

            // Send the message
            handleSend();
        }
    };

    // Runs whenever the text inside the textbox changes
    const handleInput = (
        e: React.ChangeEvent<HTMLTextAreaElement>
    ) => {

        // Update the input state
        setInput(e.target.value);

        // Automatically resize the textarea
        if (textareaRef.current) {

            // Reset the height first
            textareaRef.current.style.height = 'auto';

            // Increase the height based on the content
            textareaRef.current.style.height =
                Math.min(textareaRef.current.scrollHeight, 120) + 'px';
        }
    };

    return (

        // Main input container
        <div className="glass-elevated border-t border-white/10 p-6">

            <div className="max-w-4xl mx-auto">

                <div className="relative flex gap-3">

                    {/* Text input area */}
                    <div className="flex-1 glass rounded-2xl border-white/10 flex items-end p-4 focus-within:border-blue-500/50 smooth-transition">

                        <textarea

                            // Connect the textarea reference
                            ref={textareaRef}

                            // Display the current input
                            value={input}

                            // Update the input whenever the user types
                            onChange={handleInput}

                            // Listen for keyboard events
                            onKeyDown={handleKeyDown}

                            // Placeholder shown when empty
                            placeholder="Ask a question about your documents..."

                            // Disable typing while AI is generating a response
                            disabled={isLoading}

                            // Styling
                            className="flex-1 resize-none bg-transparent text-sm text-foreground placeholder:text-muted-foreground outline-none max-h-30"

                            // Start with one row
                            rows={1}
                        />

                    </div>

                    {/* Send Button */}
                    <Button

                        // Send the message when clicked
                        onClick={handleSend}

                        // Disable button if loading or textbox is empty
                        disabled={isLoading || !input.trim()}

                        className="flex-shrink-0 h-12 w-12 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed smooth-transition shadow-lg"
                    >

                        {/* Send icon */}
                        <Send className="w-5 h-5 text-white" />

                    </Button>

                </div>

                {/* Footer */}
                <p className="text-xs text-muted-foreground mt-3 text-center">
                    Powered by FastAPI • ChromaDB • OpenRouter • Cross Encoder
                </p>

            </div>

        </div>
    );
}