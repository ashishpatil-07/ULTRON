import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';
import logo from './chatbot-logo.png';

// Main App component
const App = () => {
  // State variables for managing user input, messages, and application states
  const [input, setInput] = useState(''); 
  const [messages, setMessages] = useState([]); 
  const messagesEndRef = useRef(null); 
  const [scrapeUrl, setScrapeUrl] = useState('');
  const [textToFind, setTextToFind] = useState(''); 
  const [linkedinMessage, setLinkedInMessage] = useState(''); 
  const [isListening, setIsListening] = useState(false); 
  const [speechRecognition, setSpeechRecognition] = useState(null); 
  const [selectedImages, setSelectedImages] = useState([]); 
  const fileInputRef = useRef(null); 
  const [isSpeaking, setIsSpeaking] = useState(false); 
  const [isLoading, setIsLoading] = useState(false); 
  const [isDarkMode, setIsDarkMode] = useState(false);
  
  // Function to reset the chat
  const resetChat = () => {
    setMessages([]); 
    setInput(''); 
    setScrapeUrl(''); 
    setTextToFind(''); 
    setLinkedInMessage(''); 
    setSelectedImages([]); 
  };

  // Toggle dark mode
  useEffect(() => {
    document.body.classList.toggle('dark-mode', isDarkMode); 
  }, [isDarkMode]);
  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => !prevMode); 
  };

  // Function to initialize speech recognition
  useEffect(() => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.onstart = () => {
      setIsListening(true); 
    };
    recognition.onend = () => {
      setIsListening(false); 
    };
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript; 
      setInput(transcript); 
    };
    setSpeechRecognition(recognition);
  }, []);

  // Function to handle voice input toggling
  const handleVoiceInput = () => {
    if (isListening) { speechRecognition.stop(); }
    else { speechRecognition.start(); }
  };

  // Function to handle scraping a URL for specific text
  const handleScrape = async () => {
    if (!scrapeUrl || !textToFind) return;
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: scrapeUrl, text_to_find: textToFind }),
      });
  
      if (!response.ok) throw new Error('Failed to scrape URL'); 
      const data = await response.json();
      const scrapeResult = `I found ${data.occurrences} occurrences of "${textToFind}":\n\n` + 
        data.examples.map(example => `- ${example}`).join('\n');
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: `Scraping "${scrapeUrl}" for "${textToFind}"`, type: 'user' },
        { text: scrapeResult, type: 'bot' },
      ]);
      setScrapeUrl(''); 
      setTextToFind(''); 
    } catch (error) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: `Error: ${error.message}`, type: 'bot' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle image file selection for LinkedIn posting
  const handleImageChange = (event) => {
    const files = Array.from(event.target.files);
    setSelectedImages(files);
  };
  // Function to handle LinkedIn post submissions
  const handleLinkedInPost = async (event) => {
    if (event?.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      if (!linkedinMessage) return;
      setIsLoading(true);
      try {
        const formData = new FormData();
        const formattedMessage = linkedinMessage.replace(/\n/g, '  \n');
        formData.append('message', formattedMessage);
        selectedImages.forEach((image) => {
          formData.append('images', image);
        });
        const response = await fetch('http://localhost:8000/linkedin/post', {
          method: 'POST',
          body: formData,
        });
        if (!response.ok) {
          throw new Error('Failed to post on LinkedIn');
        }
        const data = await response.json();
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: formattedMessage, type: 'user' },
          { text: data.message, type: 'bot' },
        ]);
        setLinkedInMessage('');
        setSelectedImages([]);
      } catch (error) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: `Error: ${error.message}`, type: 'bot' },
        ]);
      } finally {
        setIsLoading(false);
      }
    }
};

// Function to send user messages to the bot
const sendMessage = async (event) => {
  if ((event.key === 'Enter' && !event.shiftKey) || event.type === 'click') {
    event.preventDefault();
    const userMessage = input;
    if (!userMessage) return;
    const formattedUserMessage = userMessage.replace(/\n/g, '  \n'); 
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: formattedUserMessage, type: 'user' },
    ]);
    setInput('');
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });
      const data = await response.json();
      const botResponse = data.response;
      const sanitizedResponse = botResponse  
        .replace(/[^\w\s.,!?\n]/g, '')
        .replace(/\n/g, '  \n')
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: sanitizedResponse, type: 'bot' },
      ]);
    } catch (error) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: error.message, type: 'bot' },
      ]);
    } finally {
      setIsLoading(false); }
    }
  };
  
  // Function to copy text to the clipboard
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert('Copied to clipboard');
    }).catch((err) => {
      console.error('Failed to copy text: ', err);
    });
  };

  // Function to convert text to speech
  const speak = (message) => {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(message);
    utterance.lang = 'en-US'; 
    if (isSpeaking) {
      synth.cancel();
      setIsSpeaking(false);
    } else {
      synth.speak(utterance);
      setIsSpeaking(true);
      utterance.onend = () => {
        setIsSpeaking(false);
      };
    }
  };
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chat-container">
      <div className="toggle-switch" onClick={toggleDarkMode}  >
        {isDarkMode ? '☀️' : '🌙'}
      </div>
      <button 
          className="new-chat-button" 
          onClick={resetChat} 
          title="New Chat"
      >📝</button>

      <div className="chat-window">
        <h1 className="chat-title">
          <img 
            src={logo} 
            alt="logo" 
            className="logo" 
          /></h1>
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.type === 'bot' ? 'bot-response' : 'user-message'}`}>
              <div className="label">{msg.type === 'bot' ? <strong>Bot:</strong> : <strong></strong>}</div>
              <ReactMarkdown>{msg.text}</ReactMarkdown>
              {msg.type === 'bot' && (
                <div className="button-container">
                  <button className="speak-button" onClick={() => speak(msg.text)}>{isSpeaking?'🔊':'🔇'}</button>
                  <button className="copy-button" onClick={() => copyToClipboard(msg.text)}>📋</button>
                </div>
              )}
            </div>
          ))}
          {isLoading && (
          <div className="loading-indicator"></div> 
          )}
          <div ref={messagesEndRef} />
        </div>
        <div className="input-area">
          <textarea
            className="input-field"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();  
                sendMessage(e);
              }
            }}
            rows={2}
          />
            <button className="mic-button" onClick={handleVoiceInput}>{isListening ? '🔴' : '🎙️'}</button>
            <button className="send-button" onClick={sendMessage}>➤</button>
          </div>
        {/* LinkedIn post area */}
        <div className="linkedin-area">
          <textarea
            className="linkedin-input"
            placeholder="Enter LinkedIn message"
            value={linkedinMessage}
            onChange={(e) => setLinkedInMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault(); 
                handleLinkedInPost(e); }
            }}
            rows={2}
          />
          <input
            className="file-input"
            type="file"
            accept="image/*"
            multiple
            onChange={handleImageChange}
            style={{ display: 'contents' }} 
            ref={fileInputRef}
          />
          <button className="camera-button" onClick={() => fileInputRef.current.click()}>
          📷 {selectedImages.length > 0 ? `(${selectedImages.length})` : ''}
          </button>
          <button className="send-button" onClick={handleLinkedInPost}>
            Post on LinkedIn
          </button>
        </div>
        {/* URL scraping area */}
        <div className="scrape-area">
          <input
            type="text"
            className="scrape-input"
            placeholder="Enter URL to scrape"
            value={scrapeUrl}
            onChange={(e) => setScrapeUrl(e.target.value)}
          />
          <input
            type="text"
            className="scrape-input"
            placeholder="Enter text to find"
            value={textToFind}
            onChange={(e) => setTextToFind(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleScrape()}
          />
          <button className="send-button" onClick={handleScrape}>Scrape</button>
        </div>
      </div>
    </div>
  );
};

export default App;   