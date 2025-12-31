import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';
import { useAuth } from '@clerk/nextjs'; // 1. Clerk Auth ekledik
import { fetchEventSource } from '@microsoft/fetch-event-source'; // 2. Yeni kütüphaneyi ekledik

export default function Home() {
    const [idea, setIdea] = useState<string>('…loading');
    const { getToken } = useAuth(); // 3. Token alma fonksiyonunu çağırdık

    useEffect(() => {
        // Stream'i iptal etmek için (sayfa değişirse vs.) kontrolcü
        const controller = new AbortController();

        const startStream = async () => {
            try {
                // 4. Token'ı alıyoruz
                const token = await getToken();

                let isFirstChunk = true;

                // 5. Standart EventSource yerine bunu kullanıyoruz
                await fetchEventSource('/api', {
                    method: 'GET',
                    headers: {
                        // İŞTE KİLİT NOKTA: Token'ı başlığa ekliyoruz
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                    signal: controller.signal, // Bağlantıyı koparmak için gerekli

                    onmessage(msg) {
                        // Senin eski mantığın aynen burada çalışıyor
                        if (msg.data === "[DONE]") {
                            return;
                        }

                        const cleanChunk = msg.data.replace(/\\n/g, '\n');

                        setIdea((prev) => {
                            if (isFirstChunk) {
                                isFirstChunk = false;
                                return cleanChunk;
                            }
                            return prev + cleanChunk;
                        });
                    },

                    onerror(err) {
                        console.error('SSE error:', err);
                        // SADECE EĞER HİÇBİR ŞEY YAZILMADIYSA HATA MESAJI GÖSTER
                        // Eğer ekranda yarım da olsa bir metin varsa, onu silme!
                        if (isFirstChunk) {
                            setIdea("Bağlantı zaman aşımına uğradı. Lütfen tekrar deneyin.");
                        }

                        // Retrow yapmayarak retry (tekrar deneme) döngüsünü ve 403 hatalarını durdurabilirsin
                        // throw err; // <-- BUNU YORUMA AL veya SİL
                    }
                });
            } catch (err) {
                // Controller abort ettiğinde hata fırlatabilir, onu yoksayabiliriz
                console.error("Stream başlatılamadı:", err);
            }
        };

        startStream();

        // Cleanup: Sayfadan çıkılırsa bağlantıyı kes
        return () => {
            controller.abort();
        };
    }, [getToken]); // getToken bağımlılığını ekledik

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