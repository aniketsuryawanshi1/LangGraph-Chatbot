import { useState, useEffect } from "react";
import {
  BarChart3,
  MessageSquare,
  Users,
  Activity,
  RefreshCw,
} from "lucide-react";
import toast from "react-hot-toast";
import { getStatistics } from "../../services/api";
import "./StatisticsPage.css";

const StatisticsPage = () => {
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchStats = async () => {
    setIsLoading(true);
    try {
      const data = await getStatistics();
      setStats(data);
      toast.success("Statistics loaded!");
    } catch (error) {
      console.error("Error fetching statistics:", error);
      toast.error("Failed to load statistics");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const statCards = stats
    ? [
        {
          icon: MessageSquare,
          label: "Total Messages",
          value: stats.total_messages || 0,
          color: "primary",
          description: "Messages processed",
        },
        {
          icon: Users,
          label: "Active Sessions",
          value: stats.active_sessions || 0,
          color: "success",
          description: "Current sessions",
        },
        {
          icon: Activity,
          label: "Recent Sessions",
          value: stats.recent_sessions?.length || 0,
          color: "warning",
          description: "Last 5 sessions",
        },
      ]
    : [];

  return (
    <div className="statistics-page">
      <div className="statistics-container">
        {/* Header */}
        <div className="statistics-header">
          <div>
            <h1 className="page-title">Statistics Dashboard</h1>
            <p className="page-description">
              Real-time analytics and insights about chatbot usage
            </p>
          </div>
          <button
            onClick={fetchStats}
            className="btn btn-secondary"
            disabled={isLoading}
          >
            <RefreshCw className={isLoading ? "spin" : ""} size={18} />
            Refresh
          </button>
        </div>

        {isLoading && !stats ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p className="loading-text">Loading statistics...</p>
          </div>
        ) : (
          <>
            {/* Stats Cards */}
            <div className="stats-grid">
              {statCards.map((stat, index) => {
                const Icon = stat.icon;
                return (
                  <div
                    key={index}
                    className={`stat-card card stat-${stat.color}`}
                  >
                    <div className="stat-icon-wrapper">
                      <Icon className="stat-icon" size={32} />
                    </div>
                    <div className="stat-content">
                      <div className="stat-value">
                        {stat.value.toLocaleString()}
                      </div>
                      <div className="stat-label">{stat.label}</div>
                      <div className="stat-description">{stat.description}</div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Recent Sessions */}
            {stats?.recent_sessions && stats.recent_sessions.length > 0 && (
              <div className="recent-sessions card">
                <h2 className="section-title">
                  <BarChart3 size={24} />
                  Recent Sessions
                </h2>
                <div className="sessions-list">
                  {stats.recent_sessions.map((sessionId, index) => (
                    <div key={index} className="session-item">
                      <div className="session-number">{index + 1}</div>
                      <div className="session-id">
                        <span className="session-label">Session ID:</span>
                        <code>{sessionId}</code>
                      </div>
                      <a
                        href={`/history?session=${sessionId}`}
                        className="session-link"
                      >
                        View History →
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Info Cards */}
            <div className="info-grid">
              <div className="info-card card">
                <h3 className="info-title">About This Dashboard</h3>
                <p className="info-text">
                  This dashboard provides real-time insights into the chatbot's
                  performance and usage statistics. Data is updated
                  automatically and cached for optimal performance.
                </p>
              </div>

              <div className="info-card card">
                <h3 className="info-title">Technology Stack</h3>
                <ul className="tech-list">
                  <li>🧠 LangChain - Language model framework</li>
                  <li>🔄 LangGraph - DAG workflow engine</li>
                  <li>🤖 OpenAI GPT-3.5-turbo - AI model</li>
                  <li>🐘 PostgreSQL - Database</li>
                  <li>⚡ Django REST Framework - Backend API</li>
                </ul>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default StatisticsPage;
