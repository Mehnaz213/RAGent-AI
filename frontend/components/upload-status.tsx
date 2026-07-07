'use client';
// Import icons used to display different upload states
import {
    CheckCircle2,
    Loader2,
    AlertCircle,
} from 'lucide-react';

// Define the data this component receives from page.tsx
interface UploadStatusProps {

    // Name of the uploaded PDF
    fileName?: string;

    // Current upload status
    status:
    | 'idle'
    | 'processing'
    | 'success'
    | 'error';

    // Number of chunks created after processing
    chunkCount?: number;

    // Error message if upload fails
    error?: string;
}

// Create the UploadStatus component
export default function UploadStatus({

    fileName,
    status,
    chunkCount,
    error,

}: UploadStatusProps) {

    // Don't display anything when there is no upload activity
    if (status === 'idle') return null;

    return (

        // Floating notification positioned at the bottom-right corner
        <div className="fixed bottom-6 right-6 z-50">

            <div className="glass-elevated rounded-lg p-4 max-w-sm shadow-2xl">

                {/* Show while the PDF is being processed */}
                {status === 'processing' && (

                    <div className="flex items-start gap-3">

                        {/* Loading icon */}
                        <Loader2 className="w-5 h-5 text-cyan-400 animate-spin flex-shrink-0 mt-0.5" />

                        <div>

                            <p className="text-sm font-semibold text-foreground">
                                Processing PDF
                            </p>

                            {/* Uploaded filename */}
                            <p className="text-xs text-muted-foreground mt-1">
                                {fileName}
                            </p>

                            {/* Current processing stage */}
                            <p className="text-xs text-muted-foreground mt-1">
                                Chunking and generating embeddings...
                            </p>

                        </div>

                    </div>

                )}

                {/* Show when upload is successful */}
                {status === 'success' && (

                    <div className="flex items-start gap-3">

                        {/* Success icon */}
                        <CheckCircle2 className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />

                        <div>

                            {/* Success message */}
                            <p className="text-sm font-semibold text-foreground">
                                ✅ {fileName} indexed successfully.
                            </p>

                            {/* Number of chunks created */}
                            <p className="text-xs text-muted-foreground mt-1">
                                {chunkCount} chunks created.
                            </p>

                            {/* Ready message */}
                            <p className="text-xs text-green-400 font-medium mt-2">
                                Ready for querying.
                            </p>

                        </div>

                    </div>

                )}

                {/* Show when an error occurs */}
                {status === 'error' && (

                    <div className="flex items-start gap-3">

                        {/* Error icon */}
                        <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />

                        <div>

                            <p className="text-sm font-semibold text-foreground">
                                Upload Failed
                            </p>

                            {/* Error message */}
                            <p className="text-xs text-red-400 mt-1">

                                {error || 'An error occurred while processing the PDF'}

                            </p>

                        </div>

                    </div>

                )}

            </div>

        </div>

    );
}