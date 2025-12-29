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
        <main className="min-h-screen bg-gray-50 dark:bg-gray-900 py-10 px-4">
            <div className="max-w-3xl mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
                
                {/* Başlık Alanı */}
                <div className="p-6 border-b border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-900/50">
                    <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-100 flex items-center gap-2">
                        🤖 AI Business Generator
                        {/* Yanıp sönen imleç efekti (opsiyonel) */}
                        {idea === '…loading' && <span className="animate-pulse">...</span>}
                    </h1>
                </div>

                {/* İÇERİK ALANI - BURASI ÖNEMLİ */}
                <div className="p-8">
                    {/* 'prose' sınıfı: Markdown'ı otomatik stillendirir.
                        'prose-lg': Yazıyı biraz büyütür.
                        'dark:prose-invert': Koyu modda yazıların rengini otomatik açar.
                    */}
                    <article className="prose prose-lg prose-slate dark:prose-invert max-w-none leading-relaxed">
                        <ReactMarkdown 
                            remarkPlugins={[remarkGfm, remarkBreaks]}
                            components={{
                                // Linklerin yeni sekmede açılmasını istersen:
                                a: ({node, ...props}) => <a {...props} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline" />
                            }}
                        >
                            {idea}
                        </ReactMarkdown>
                    </article>
                </div>
                
            </div>
        </main>
    );
}