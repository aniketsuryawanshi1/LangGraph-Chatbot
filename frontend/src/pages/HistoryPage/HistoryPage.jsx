import { useState } from "react";
import { Search, Clock, Trash2, Download } from "lucide-react";
import toast from "react-hot-toast";
import { getSessionHistory, clearSession } from "../../services/api";
import "./HistoryPage.css";

const HistoryPage = () => {
  const [sessionId, setSessionId] = useState("");
  const [history, setHistory] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!sessionId.trim()) {
      toast.error("Please enter a session ID");
      return;
    }

    setIsLoading(true);

    try {
      const response = await getSessionHistory(sessionId.trim());

      if (response.success && response.history.length > 0) {
        setHistory(response);
        toast.success("History loaded successfully!");
      } else {
        setHistory({ success: true, history: [] });
        toast.info("No history found for this session");
      }
    } catch (error) {
      console.error("Error fetching history:", error);
      toast.error("Failed to fetch history. Please check the session ID.");
      setHistory(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearHistory = async () => {
    if (!sessionId) return;

    if (!confirm("Are you sure you want to clear this session history?")) {
      return;
    }

    try {
      await clearSession(sessionId);
      setHistory(null);
      setSessionId("");
      toast.success("History cleared successfully!");
    } catch (error) {
      console.error("Error clearing history:", error);
      toast.error("Failed to clear history");
    }
  };

  const handleExport = () => {
    if (!history || history.history.length === 0) return;

    const data = JSON.stringify(history.history, null, 2);
    const blob = new Blob([data], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `chat-history-${sessionId}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    toast.success("History exported!");
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="history-page">
      <div className="history-container">
        <div className="history-header">
          <h1 className="page-title">Conversation History</h1>
          <p className="page-description">
            Search and view your conversation history by session ID
          </p>
        </div>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="search-form">
          <div className="search-input-group">
            <Search className="search-icon" size={20} />
            <input
              type="text"
              value={sessionId}
              onChange={(e) => setSessionId(e.target.value)}
              placeholder="Enter session ID (e.g., session-abc123...)"
              className="search-input"
              disabled={isLoading}
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={isLoading}
          >
            {isLoading ? "Searching..." : "Search"}
          </button>
        </form>

        {/* History Results */}
        {history && (
          <div className="history-results">
            <div className="results-header">
              <div className="results-info">
                <h2>Session: {sessionId.slice(0, 20)}...</h2>
                <p>{history.history.length} message(s) found</p>
                {history.source && (
                  <span className="badge badge-primary">
                    Source: {history.source}
                  </span>
                )}
              </div>
              <div className="results-actions">
                <button
                  onClick={handleExport}
                  className="btn btn-secondary"
                  disabled={history.history.length === 0}
                >
                  <Download size={18} />
                  Export
                </button>
                <button onClick={handleClearHistory} className="btn btn-danger">
                  <Trash2 size={18} />
                  Clear
                </button>
              </div>
            </div>

            {history.history.length === 0 ? (
              <div className="empty-state">
                <Clock size={60} className="empty-state-icon" />
                <h3>No History Found</h3>
                <p>This session has no conversation history yet.</p>
              </div>
            ) : (
              <div className="history-list">
                {history.history.map((message, index) => (
                  <div
                    key={index}
                    className={`history-message ${message.type}`}
                  >
                    <div className="message-header">
                      <span className="message-type">
                        {message.type === "user" ? "👤 You" : "🤖 Bot"}
                      </span>
                      <span className="message-timestamp">
                        {formatTimestamp(message.timestamp)}
                      </span>
                    </div>
                    <div className="message-body">{message.content}</div>
                    {message.query_type && (
                      <div className="message-footer">
                        <span className={`badge badge-${message.query_type}`}>
                          {message.query_type}
                        </span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Initial State */}
        {!history && !isLoading && (
          <div className="empty-state">
            <Clock size={80} className="empty-state-icon" />
            <h2>Search Conversation History</h2>
            <p>Enter a session ID above to view your chat history</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryPage;
