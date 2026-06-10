import { useState } from 'react';
import axios from 'axios';

function App() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ prediction: string, confidence: number, suspicious_words?: string[] } | null>(null);
  const [error, setError] = useState('');
  const [showHowItWorks, setShowHowItWorks] = useState(false);

  const loadPhishingExample = () => {
    setText("URGENT: Your M-Pesa account has been suspended. Click here to verify your identity http://mpesa-verify.duckdns.org/verify?id=8271 Failure to do so within 24 hours will result in permanent account closure.");
  };

  const loadLegitimateExample = () => {
    setText("Hi team, please find attached the quarterly report. Let me know if you have any questions before our meeting on Friday at 10 AM.");
  };

  const handleClear = () => {
    setText('');
    setResult(null);
    setError('');
  };

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError('Please enter a message to analyze.');
      return;
    }
    setError('');
    setLoading(true);
    setResult(null);
    
    try {
      const response = await axios.post('http://localhost:5000/predict', { text });
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to connect to the analysis engine.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 font-sans">
      <div className="w-full max-w-5xl">
        <header className="mb-12 flex flex-col items-center text-center">
          <div className="inline-block border border-gray-200 bg-gray-50 text-[10px] font-bold uppercase tracking-[0.25em] px-4 py-1.5 mb-5 rounded-full text-orange-600">
            AI Analysis Engine
          </div>
          <h1 className="text-4xl md:text-5xl font-black tracking-tighter text-black leading-tight">
            Phishing Detector<span className="text-orange-500">.</span>
          </h1>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          {/* LEFT SIDE: Input Form */}
          <div className="bg-white p-8 md:p-10 rounded-sm shadow-md border-2 border-black flex flex-col h-full">
            <div className="mb-4 flex-grow">
              <label htmlFor="message" className="block text-sm font-semibold text-black mb-3">
                Message Content
              </label>
              <textarea
                id="message"
                rows={7}
                className="w-full bg-gray-50 border border-gray-200 p-5 text-black placeholder-gray-400 focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 rounded-sm resize-none transition-all duration-300"
                placeholder="Paste the suspicious message here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
              />
              {error && (
                <p className="text-red-600 font-medium text-sm mt-3">
                  {error}
                </p>
              )}
            </div>
            
            <div className="flex flex-wrap gap-3 mb-8 w-full">
              <button onClick={loadPhishingExample} className="text-[10px] md:text-xs font-bold uppercase tracking-widest text-gray-500 hover:text-orange-600 transition-colors bg-gray-100 hover:bg-orange-50 px-3 py-2 rounded-sm border border-transparent hover:border-orange-200">
                Load Phishing Example
              </button>
              <button onClick={loadLegitimateExample} className="text-[10px] md:text-xs font-bold uppercase tracking-widest text-gray-500 hover:text-orange-600 transition-colors bg-gray-100 hover:bg-orange-50 px-3 py-2 rounded-sm border border-transparent hover:border-orange-200">
                Load Legitimate Example
              </button>
              <button onClick={handleClear} disabled={!text && !result} className="ml-auto text-[10px] md:text-xs font-bold uppercase tracking-widest text-gray-400 hover:text-black transition-colors bg-white hover:bg-gray-100 px-3 py-2 rounded-sm border border-gray-200 disabled:opacity-30 disabled:cursor-not-allowed">
                Clear
              </button>
            </div>

            <button
              onClick={handleAnalyze}
              disabled={loading || !text.trim()}
              className="w-full bg-orange-500 text-white font-bold uppercase tracking-widest py-4 px-6 hover:bg-orange-600 transition-all duration-300 disabled:opacity-30 disabled:cursor-not-allowed rounded-sm shadow-md hover:shadow-xl"
            >
              {loading ? 'Analyzing...' : 'Analyze Message'}
            </button>
          </div>

          {/* RIGHT SIDE: Results and Info */}
          <div className="flex flex-col gap-8 h-full">
            
            {/* Results Box */}
            <div className="bg-white p-8 md:p-10 rounded-sm shadow-md border-2 border-black flex-grow transition-all duration-500 flex flex-col justify-center">
              {!result && !loading && (
                <div className="text-center text-gray-400">
                  <div className="text-6xl mb-4 opacity-20">⚙️</div>
                  <p className="text-sm font-semibold uppercase tracking-widest">Awaiting Analysis</p>
                  <p className="text-xs mt-2">Paste a message and click Analyze to see the results here.</p>
                </div>
              )}

              {loading && (
                <div className="text-center text-orange-500 animate-pulse">
                  <div className="text-4xl mb-4">...</div>
                  <p className="text-sm font-bold uppercase tracking-widest">Processing Data</p>
                </div>
              )}

              {result && (
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 w-full">
                  <div className="text-center mb-6">
                    <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-2">Result</h3>
                    <p className="text-3xl font-black text-black uppercase">
                      {result.prediction === 'phishing' ? 'Phishing Attempt' : 'Legitimate Message'}
                    </p>
                  </div>
                  
                  <div className="text-center">
                    <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-2">AI Confidence</h3>
                    <p className="text-5xl font-black text-orange-500">{result.confidence}%</p>
                  </div>
                  
                  <div className="w-full bg-gray-100 h-2 mt-8 rounded-sm overflow-hidden">
                    <div 
                      className="h-full bg-orange-500 transition-all duration-1000 ease-out"
                      style={{ width: `${result.confidence}%` }}
                    />
                  </div>

                  {/* Explainable AI - Highlighted Suspicious Words */}
                  {result.prediction === 'phishing' && result.suspicious_words && result.suspicious_words.length > 0 && (
                    <div className="mt-8 pt-6 border-t border-gray-100/50">
                      <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-4">Suspicious Keywords Detected</h3>
                      <div className="flex flex-wrap gap-2">
                        {result.suspicious_words.map((word, idx) => (
                          <span key={idx} className="bg-orange-100 text-orange-700 text-[10px] font-bold uppercase tracking-widest px-3 py-1.5 rounded-sm border border-orange-200">
                            {word}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* How it Works Accordion */}
            <div>
              <button 
                onClick={() => setShowHowItWorks(!showHowItWorks)}
                className="w-full bg-white p-6 rounded-sm shadow-sm border-2 border-black flex justify-between items-center hover:bg-gray-50 transition-colors"
              >
                <span className="text-sm font-bold uppercase tracking-widest text-black">How does the AI work?</span>
                <span className="text-xl font-light text-orange-500">{showHowItWorks ? '−' : '+'}</span>
              </button>
              
              {showHowItWorks && (
                <div className="bg-white border-x-2 border-b-2 border-black p-8 rounded-b-sm shadow-sm text-sm text-gray-600 leading-relaxed mt-[-2px]">
                  <ol className="list-decimal list-inside space-y-4">
                    <li><strong className="text-black">Preprocessing:</strong> The backend receives the text, converts it to lowercase, removes punctuation, and filters out common stop words.</li>
                    <li><strong className="text-black">TF-IDF Vectorization:</strong> The cleaned text is converted into a numerical vector using Term Frequency-Inverse Document Frequency, which highlights words that are statistically important to the message.</li>
                    <li><strong className="text-black">Logistic Regression:</strong> A trained machine learning model analyzes the feature vector against historical patterns of phishing and legitimate messages to produce a probability score.</li>
                  </ol>
                </div>
              )}
            </div>
            
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
