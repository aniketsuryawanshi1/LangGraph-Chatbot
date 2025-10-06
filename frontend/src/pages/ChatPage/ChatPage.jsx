import { useState, useRef, useEffect } from "react";
import { Send, Loader, Bot, User, Trash2 } from "lucide-react";
import toast from "react-hot-toast";
import { sendMessage, clearSession } from "../../services/api";
import "./ChatPage.css";

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");

    // Add user message to UI
    const newUserMessage = {
      type: "user",
      content: userMessage,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, newUserMessage]);

    setIsLoading(true);

    try {
      const response = await sendMessage(userMessage, sessionId);

      if (response.success) {
        // Save session ID
        if (!sessionId) {
          setSessionId(response.session_id);
        }

        // Add bot response
        const botMessage = {
          type: "bot",
          content: response.response,
          query_type: response.query_type,
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, botMessage]);

        toast.success("Response received!");
      } else {
        toast.error(response.error || "Failed to get response");
      }
    } catch (error) {
      console.error("Error sending message:", error);
      toast.error("Failed to send message. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = async () => {
    if (!sessionId) {
      setMessages([]);
      toast.success("Chat cleared!");
      return;
    }

    try {
      await clearSession(sessionId);
      setMessages([]);
      setSessionId(null);
      toast.success("Chat history cleared!");
    } catch (error) {
      console.error("Error clearing chat:", error);
      toast.error("Failed to clear chat");
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="chat-page">
      <div className="chat-container">
        {/* Chat Header */}
        <div className="chat-header">
          <div className="chat-header-info">
            <Bot className="header-icon" size={28} />
            <div>
              <h1 className="chat-title">Smart Chatbot</h1>
              <p className="chat-subtitle">
                {sessionId
                  ? `Session: ${sessionId.slice(0, 12)}...`
                  : "Start a new conversation"}
              </p>
            </div>
          </div>

          {messages.length > 0 && (
            <button
              onClick={handleClearChat}
              className="btn-clear"
              title="Clear chat"
            >
              <Trash2 size={20} />
              <span>Clear</span>
            </button>
          )}
        </div>

        {/* Chat Messages */}
        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="empty-chat">
              <Bot size={80} className="empty-icon" />
              <h2>Start a Conversation</h2>
              <p>
                Ask me anything! I can help with questions, calculations, and
                more.
              </p>
              <div className="suggestion-chips">
                <button
                  className="chip"
                  onClick={() => setInput("What can you do?")}
                >
                  What can you do?
                </button>
                <button
                  className="chip"
                  onClick={() => setInput("Calculate 15 * 24")}
                >
                  Calculate 15 * 24
                </button>
                <button
                  className="chip"
                  onClick={() => setInput("Tell me about LangChain")}
                >
                  Tell me about LangChain
                </button>
              </div>
            </div>
          ) : (
            <>
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`message ${
                    message.type === "user" ? "user-message" : "bot-message"
                  }`}
                >
                  <div className="message-avatar">
                    {message.type === "user" ? (
                      <User size={20} />
                    ) : (
                      <Bot size={20} />
                    )}
                  </div>
                  <div className="message-content">
                    <div className="message-text">{message.content}</div>
                    <div className="message-meta">
                      <span className="message-time">
                        {formatTime(message.timestamp)}
                      </span>
                      {message.query_type && (
                        <span className={`badge badge-${message.query_type}`}>
                          {message.query_type}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="message bot-message">
                  <div className="message-avatar">
                    <Bot size={20} />
                  </div>
                  <div className="message-content">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Chat Input */}
        <div className="chat-input-container">
          <form onSubmit={handleSendMessage} className="chat-input-form">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="chat-input"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="btn-send"
              disabled={!input.trim() || isLoading}
            >
              {isLoading ? (
                <Loader className="spin" size={20} />
              ) : (
                <Send size={20} />
              )}
            </button>
          </form>
          <p className="input-hint">
            Press Enter to send • Supports text queries and calculations
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
