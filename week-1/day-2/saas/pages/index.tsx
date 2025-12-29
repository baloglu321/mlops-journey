"use client"

import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';

export default function Home() {
    const [idea, setIdea] = useState<string>('…loading');

    useEffect(() => {
        const evt = new EventSource('/api');
        
        // Bu değişken hafızada tutulacak ve ilk mesaj geldiğinde kontrol edilecek
        let isFirstChunk = true; 

        evt.onmessage = (e) => {
            // 1. Konsola basalım ki veri geliyor mu görelim (F12 -> Console)
            // console.log("Gelen parça:", e.data);

            if (e.data === "[DONE]") {
                evt.close();
                return;
            }

            // Backend'den gelen \n karakterlerini düzelt
            const cleanChunk = e.data.replace(/\\n/g, '\n');

            setIdea((prev) => {
                // Eğer bu ilk gelen parçaysa, önceki "loading" yazısını tamamen sil ve yeni parçayı koy
                if (isFirstChunk) {
                    isFirstChunk = false; // Artık ilk parça değil
                    return cleanChunk;
                }
                // İlk parça değilse, var olanın üzerine ekle
                return prev + cleanChunk;
            });
        };

        evt.onerror = (err) => {
            console.error('SSE error:', err);
            evt.close();
            if (isFirstChunk) {
                setIdea("Bağlantı hatası oluştu veya sunucu cevap vermedi.");
            }
        };

        return () => { evt.close(); };
    }, []);

    return (
        <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
            <div className="container mx-auto px-4 py-12">
                
                 {/* Header */}
                 <header className="text-center mb-12">
                    <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
                        Business Idea Generator
                    </h1>
                    <p className="text-gray-600 dark:text-gray-400 text-lg">
                        AI-powered innovation at your fingertips
                    </p>
                </header>

                 {/* Content Card */}
                 <div className="max-w-3xl mx-auto">
                    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 backdrop-blur-lg bg-opacity-95">
                        {idea === '…loading' ? (
                            <div className="flex items-center justify-center py-12">
                                <div className="animate-pulse text-gray-400">
                                    Generating your business idea...
                                </div>
                            </div>
                        ) : (
                            <div className="markdown-content text-gray-700 dark:text-gray-300">
                                <ReactMarkdown
                                    remarkPlugins={[remarkGfm, remarkBreaks]}
                                >
                                    {idea}
                                </ReactMarkdown>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </main>
    );
}