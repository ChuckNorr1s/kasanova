'use client';

import { useState, useRef, useEffect } from 'react';
import { Plus, Search, MapPin, Image, FileText, Lightbulb, ListTodo, MoreHorizontal, ArrowUp, Code, Palette, Zap, Loader2 } from 'lucide-react';


type ChatMessage = {
  id: number;
  sender: 'user' | 'bot';
  content: string;
  isFinal?: boolean;
};


function ActionButton({ icon, text }: { icon: React.ReactNode; text: string }) {
  return (
    <button className="px-4 py-2 bg-white hover:bg-amber-50 rounded-full transition-colors flex items-center gap-2 shadow-sm">
      <span className="text-amber-600">{icon}</span>
      <span className="text-sm text-gray-700">{text}</span>
    </button>
  );
}

export default function Chat() {
  const [message, setMessage] = useState('');
  const [doctrine, setDoctrine] = useState('');
  const [reason, setReason] = useState('');
  const [showMore, setShowMore] = useState(false);
  const [showSearchPopup, setShowSearchPopup] = useState(false);
  const [showReasonPopup, setShowReasonPopup] = useState(false);
  const [showPlusTooltip, setShowPlusTooltip] = useState(false);
  const [data, setData] = useState('');
  const [query, setQuery] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [tips, setTips] = useState(true);
  
  // Create refs for the desktop and mobile textareas.
  const desktopTextAreaRef = useRef<HTMLTextAreaElement>(null);
  const mobileTextAreaRef = useRef<HTMLTextAreaElement>(null);
  // Separate refs for the Doctrine and Reason popups.
  const doctrineContainerRef = useRef<HTMLDivElement>(null);
  const reasonContainerRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const streamIdRef = useRef<number>(0);


  // Helper function to update the textarea value.
  const handleActionClick = (actionText: string) => {
    setMessage(`${actionText} `);
    if (desktopTextAreaRef.current) {
      desktopTextAreaRef.current.focus();
    } else if (mobileTextAreaRef.current) {
      mobileTextAreaRef.current.focus();
    }
  };

  // Send handler: adds user message, adds a bot message placeholder, sets query, and clears input.
  const handleSend = () => {
    // Проверка за празен стринг или съобщение само с whitespace
  if (!message.trim() || message.split(/\s+/).filter(word => word.length > 0).length === 0) {
    return;
  }
    setIsStreaming(true);
    if (!message.trim()) return;
    const userMsg: ChatMessage = { 
      id: Date.now(), 
      sender: 'user', 
      content: message 
    };
    setChatMessages((prev) => [...prev, userMsg]);
    setQuery(message);
    setMessage('');
    setTips(false);
  };

  // Close the Doctrine popup if the user clicks outside its container.

  // deprecated
  /*
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        doctrineContainerRef.current &&
        !doctrineContainerRef.current.contains(event.target as Node)
      ) {
        setShowSearchPopup(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);
  */

  // Close the Reason popup if the user clicks outside its container.
  /*
    //deprecated
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        reasonContainerRef.current &&
        !reasonContainerRef.current.contains(event.target as Node)
      ) {
        setShowReasonPopup(false);
        console.log("clicked on: " + event.target);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);
    
    */


   useEffect(() => {
    const fetchStream = async () => {
      const queryParam = query || 'What is the meaning of life?';
      const toxicityParam = reason || '0.0';
      const doctrineParam = doctrine || 'Reinvest for Revolution';
      
      const url = `/api/stream?query=${encodeURIComponent(queryParam)}&toxicity=${toxicityParam}&doctrine=${doctrineParam}`;
      
      const response = await fetch(url);
      const reader = response.body?.getReader();
      const decoder = new TextDecoder('utf-8');
      let streamId = ++streamIdRef.current;

      if (!reader) return;

      const readChunk = async () => {
        if (streamId !== streamIdRef.current) return;
        
        const { done, value } = await reader.read();
        if (done) {
          setIsStreaming(false);
  setChatMessages(prev => {
    // Find the index of the last bot message that is not final
    let lastBotMsgIndex = -1;
    for (let i = prev.length - 1; i >= 0; i--) {
      if (prev[i].sender === 'bot' && !prev[i].isFinal) {
        lastBotMsgIndex = i;
        break;
      }
    }
    // If found, update only that message
    if (lastBotMsgIndex !== -1) {
      const newMessages = [...prev];
      newMessages[lastBotMsgIndex] = {
        ...newMessages[lastBotMsgIndex],
        isFinal: true
      };
      return newMessages;
    }
    return prev;
  });
  return;
}

        const chunk = decoder.decode(value);
        setChatMessages(prev => [
          ...prev,
          {
            id: Date.now(),
            sender: 'bot',
            content: chunk,
            isFinal: false
          }
        ]);

        readChunk();
      };

      readChunk();
    };

    if (query) {
      fetchStream();
    }

    return () => {
      streamIdRef.current++; // Invalidate previous streams
    };
  }, [query]);


  useEffect(() => {
  messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
}, [query]);



  return (
    <div className="min-h-screen bg-white flex flex-col">

      {/* Chat Messages */}
      {!tips && (
        <div className="flex flex-col self-center md:w-3/4 xl:w-1/2 max-w-3xl p-4 mt-16 mb-32 whitespace-pre-wrap">
        {chatMessages.map((msg) => {
  // Determine the classes for each message
  const userClasses = "rounded-lg bg-[#eff6ff] text-base text-[#262626] self-end shadow-sm mb-2 p-3";
  const botClasses = msg.isFinal 
    ? "text-[#262626] text-base border-none self-start my-5" // Final bot message color
    : "text-[#8B8B89] text-sm self-start border-l-2 border-[#e5e5e5] p-3"; // Default bot message color

  return (
    <div
      key={msg.id}
      className={`${msg.sender === 'user' ? userClasses : botClasses}`}
    >
      {msg.content}
    </div>
  );
})}
        {isStreaming && (
          <Loader2 className="animate-spin w-7 h-7 text-gray-400" />
        )}
        
      </div>
      )}


      {/* Main Content */}
      <div className="flex-1 p-4 md:p-8 flex flex-col md:justify-center items-center">
        <div className="w-full max-w-3xl flex flex-col items-center gap-8">
          {tips && (
            <>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">What can I help with?</h1>

          {/* Action Buttons */}
          <div className="w-full flex flex-wrap gap-2 justify-center">
            <div onClick={() => handleActionClick("Create image")}><ActionButton icon={<Image />} text="Create image" /></div>
            <div onClick={() => handleActionClick("Summarize text")}><ActionButton icon={<FileText />} text="Summarize text" /></div>
            <div onClick={() => handleActionClick("Brainstorm")}><ActionButton icon={<Lightbulb />} text="Brainstorm" /></div>
            <div onClick={() => handleActionClick("Make a plan")}><ActionButton icon={<ListTodo />} text="Make a plan" /></div>
            
              
              {!showMore && (
                <>
                <button 
              className="px-4 py-2 text-gray-600 hover:bg-white/50 rounded-full transition-colors flex items-center gap-2"
              onClick={() => setShowMore(!showMore)}
            >
                <MoreHorizontal className="w-4 h-4" />
                <span className="text-sm">More</span>
                </button>
                </>
              )} 
            {showMore && (
              <>
                <div onClick={() => handleActionClick("Write code")}><ActionButton icon={<Code />} text="Write code" /></div>
                <div onClick={() => handleActionClick("Design UI")}><ActionButton icon={<Palette />} text="Design UI" /></div>
                <div onClick={() => handleActionClick("Optimize")}><ActionButton icon={<Zap />} text="Optimize" /></div>
              </>
            )}
          </div>
            </>
          )}

          {tips && (
            <>
            {/* Desktop Chat Input - Hidden on mobile */}
          <div className="hidden md:block w-full">
            <div className="relative rounded-2xl shadow-lg p-3">
              <textarea
                disabled={isStreaming}
                ref={desktopTextAreaRef}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                placeholder="Message KASANOVA"
                className="w-full min-h-[56px] px-4 py-3 text-gray-700 rounded-xl bg-white border-gray-200 border-none focus:outline-none focus:border-amber-500 resize-none"
              />
              <div className="flex items-center justify-between px-2 py-1">
                <div className="flex items-center sm:gap-2">
                  <div className="relative inline-block">
                    <button
                      onMouseOverCapture={() => { setShowPlusTooltip(true); }}
                      onMouseLeave={() => { setTimeout(() => setShowPlusTooltip(false), 150); }}
                      className="p-2 hover:bg-amber-100 rounded-lg transition-colors"
                    >
                      <Plus className="w-5 h-5 text-gray-500" />
                    </button>
                    {showPlusTooltip && (
                      <div className="relative inline-block">
                      <div className="absolute top-2 right-3 transform -translate-y-1 rotate-45 w-3 h-3 bg-[linear-gradient(#f851491a,#f851491a)] border-t border-l border-[#f85149]"></div>
                      <div className="absolute top-0 left-1/2 transform -translate-x-1/2 mt-3 px-2 py-1 text-lg border border-[#f85149] text-[#b22b2b] bg-[linear-gradient(#f851491a,#f851491a)] rounded">
                      Coming Soon
                      </div>
                      </div>
                    )}
                  </div>
                  {/* Doctrine Popup */}
                  <div ref={doctrineContainerRef} className="relative inline-block">
                    <button
                      onClick={() => setShowSearchPopup((prev) => !prev)}
                      className="flex items-center gap-1 px-3 py-1.5 text-gray-600 hover:bg-amber-100 rounded-lg transition-colors"
                    >
                      <Search className="w-4 h-4" />
                      <span className="text-sm">Doctrine</span>
                    </button>
                    {showSearchPopup && (
                      <div className="absolute top-full left-0 z-10">
                        {/* Tooltip arrow */}
                        <div className="relative">
                          <div className="absolute top-0 left-4 w-3 h-3 bg-white border-t border-l border-gray-300 transform rotate-45 -translate-y-1"></div>
                          <div className="mt-2 w-48 bg-white border border-gray-300 rounded-md shadow-md p-2">
                            <input
                              value={doctrine}
                              onChange={(e) => setDoctrine(e.target.value)}
                              type="text"
                              placeholder="Quantum Doctrine 🧠"
                              className="w-full p-1 border border-gray-300 rounded-md focus:outline-none focus:border-amber-500"
                            />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                  {/* Reason Popup */}
                  <div ref={reasonContainerRef} className="relative inline-block">
                    <button
                      onClick={() => setShowReasonPopup((prev) => !prev)}
                      className="flex items-center gap-1 px-3 py-1.5 text-gray-600 hover:bg-amber-100 rounded-lg transition-colors"
                    >
                      <MapPin className="w-4 h-4" />
                      <span className="text-sm">Toxicity</span>
                    </button>
                    {showReasonPopup && (
                      <div className="absolute top-full left-0 z-10">
                        {/* Tooltip arrow */}
                        <div className="relative">
                          <div className="absolute top-0 left-4 w-3 h-3 bg-white border-t border-l border-gray-300 transform rotate-45 -translate-y-1"></div>
                          <div className="mt-2 w-48 bg-white border border-gray-300 rounded-md shadow-md p-2">
                            <input
                              value={reason}
                              onChange={(e) => setReason(e.target.value)}
                              type="number"
                              placeholder="Toxicity Amplifier 🔢"
                              className="w-full p-1 border border-gray-300 rounded-md focus:outline-none focus:border-amber-500"
                            />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
                <button onClick={handleSend} aria-disabled={isStreaming} className="p-2 disabled:opacity-50 bg-amber-500 hover:bg-amber-600 rounded-lg transition-colors">
                  {isStreaming ? (
                    <Loader2 className="animate-spin w-5 h-5 text-white" />
                  ) : (
                    <ArrowUp className="w-5 h-5 text-white" />
                  )}
                </button>
              </div>
            </div>
          </div>
            </>
          )}
        </div>
      </div>

          <div ref={messagesEndRef} />
      {/* Mobile Chat Input/After sending 1st message - Hidden on desktop */}
            <div className={`${tips ? 'md:hidden' : 'md:fixed'} mb-4 w-full md:w-3/4 xl:w-2/5 self-center fixed bottom-0 bg-white`}>
            <div className="relative rounded-2xl shadow-lg p-3">
              <textarea
                disabled={isStreaming}
                ref={desktopTextAreaRef}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSend();
                    }
                  }}
                placeholder="Message KASANOVA"
                className="w-full min-h-[56px] px-4 py-3 text-gray-700 rounded-xl bg-white border-gray-200 border-none focus:outline-none focus:border-amber-500 resize-none"
              />
              <div className="flex items-center justify-between px-2 py-1">
                <div className="flex items-center sm:gap-2">
                  <div className="relative inline-block">
                    <button
                      onMouseOverCapture={() => { setShowPlusTooltip(true); }}
                      onMouseLeave={() => { setTimeout(() => setShowPlusTooltip(false), 150); }}
                      className="p-2 hover:bg-amber-50 rounded-lg transition-colors"
                    >
                      <Plus className="w-5 h-5 text-gray-500" />
                    </button>
                    {showPlusTooltip && (
                      <div className="relative inline-block">
                      <div className="absolute -top-9 right-3 transform -translate-y-1 -rotate-[135deg] w-3 h-3 bg-[linear-gradient(#f851491a,#f851491a)] border-t border-l border-[#f85149]"></div>
                      <div className="text-lg absolute -top-28 left-1/2 transform -translate-x-1/2 mt-3 px-2 py-1 border border-[#f85149] text-[#b22b2b] bg-[linear-gradient(#f851491a,#f851491a)] rounded">
                      Coming Soon
                      </div>
                      </div>
                    )}
                  </div>
                  {/* Doctrine Popup */}
                  <div ref={doctrineContainerRef} className="relative inline-block">
                    <button
                      onClick={() => setShowSearchPopup((prev) => !prev)}
                      className="flex items-center gap-1 px-3 py-1.5 text-gray-600 hover:bg-amber-50 rounded-lg transition-colors"
                    >
                      <Search className="w-4 h-4" />
                      <span className="text-sm">Doctrine</span>
                    </button>
                    {showSearchPopup && (
                      <div className="absolute top-full left-0 z-10">
                        {/* Tooltip arrow */}
                        <div className="relative">
                          <div className="absolute -top-10 left-4 w-3 h-3 bg-white border-t border-l border-gray-300 transform -rotate-[135deg] -translate-y-1"></div>
                          <div className="absolute -top-24 mt-2 w-48 bg-white border border-gray-300 rounded-md shadow-md p-2">
                            <input
                              value={doctrine}
                              onChange={(e) => setDoctrine(e.target.value)}
                              type="text"
                              placeholder="Quantum Doctrine 🧠"
                              className="w-full p-1 border border-gray-300 rounded-md focus:outline-none focus:border-amber-500"
                            />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                  {/* Reason Popup */}
                  <div ref={reasonContainerRef} className="relative inline-block">
                    <button
                      onClick={() => setShowReasonPopup((prev) => !prev)}
                      className="flex items-center gap-1 px-3 py-1.5 text-gray-600 hover:bg-amber-50 rounded-lg transition-colors"
                    >
                      <MapPin className="w-4 h-4" />
                      <span className="text-sm">Toxicity</span>
                    </button>
                    {showReasonPopup && (
                      <div className="absolute top-full left-0 z-10">
                        {/* Tooltip arrow */}
                        <div className="relative">
                          <div className="absolute -top-10 left-4 w-3 h-3 bg-white border-t border-l border-gray-300 transform -rotate-[135deg] -translate-y-1"></div>
                          <div className="absolute -top-24 -left-12 mt-2 w-48 bg-white border border-gray-300 rounded-md shadow-md p-2">
                            <input
                              value={reason}
                              onChange={(e) => setReason(e.target.value)}
                              type="number"
                              placeholder="Toxicity Amplifier 🔢"
                              className="w-full p-1 border border-gray-300 rounded-md focus:outline-none focus:border-amber-500"
                            />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
                <button onClick={handleSend} aria-disabled={isStreaming} className="p-2 disabled:opacity-50 bg-amber-500 hover:bg-amber-600 rounded-lg transition-colors">
                  {isStreaming ? (
                    <Loader2 className="animate-spin w-5 h-5 text-white" />
                  ) : (
                    <ArrowUp className="w-5 h-5 text-white" />
                  )}
                </button>
              </div>
            </div>
          </div>

      
    </div>
  );
}