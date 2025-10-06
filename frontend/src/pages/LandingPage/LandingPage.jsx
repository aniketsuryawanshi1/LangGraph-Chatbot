import { Link } from "react-router-dom";
import {
  MessageSquare,
  Zap,
  Brain,
  Shield,
  ArrowRight,
  CheckCircle,
  Sparkles,
} from "lucide-react";
import "./LandingPage.css";

const LandingPage = () => {
  const features = [
    {
      icon: Brain,
      title: "LangChain Powered",
      description:
        "Built with LangChain for advanced language model interactions and memory management.",
    },
    {
      icon: Zap,
      title: "LangGraph Workflow",
      description:
        "Utilizes LangGraph DAG for intelligent query routing and processing workflows.",
    },
    {
      icon: MessageSquare,
      title: "Smart Conversations",
      description:
        "Context-aware conversations with memory that remembers your chat history.",
    },
    {
      icon: Shield,
      title: "Secure & Private",
      description:
        "Your data is encrypted and stored securely with PostgreSQL database.",
    },
  ];

  const capabilities = [
    "Natural language understanding",
    "Mathematical calculations",
    "Context-aware responses",
    "Conversation history",
    "Real-time processing",
    "Multi-session support",
  ];

  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-badge">
            <Sparkles size={16} />
            <span>Powered by OpenAI GPT-3.5-turbo</span>
          </div>

          <h1 className="hero-title animate-fade-in">
            Experience the Future of
            <span className="text-gradient"> AI Conversations</span>
          </h1>

          <p className="hero-description animate-fade-in">
            A smart, intelligent chatbot built with cutting-edge technologies
            like LangChain, LangGraph, and OpenAI. Get instant answers, perform
            calculations, and enjoy natural conversations with advanced AI.
          </p>

          <div className="hero-actions animate-fade-in">
            <Link to="/chat" className="btn btn-primary btn-large">
              Start Chatting
              <ArrowRight size={20} />
            </Link>
            <Link to="/statistics" className="btn btn-secondary btn-large">
              View Statistics
            </Link>
          </div>

          <div className="hero-stats">
            <div className="stat-item">
              <div className="stat-number">10k+</div>
              <div className="stat-label">Messages Processed</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">99.9%</div>
              <div className="stat-label">Uptime</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">&lt;1s</div>
              <div className="stat-label">Response Time</div>
            </div>
          </div>
        </div>

        <div className="hero-illustration">
          <div className="floating-card card-1">
            <MessageSquare size={24} />
            <p>How can I help you today?</p>
          </div>
          <div className="floating-card card-2">
            <Brain size={24} />
            <p>Processing with AI...</p>
          </div>
          <div className="floating-card card-3">
            <Zap size={24} />
            <p>Lightning fast responses</p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="section-header">
          <h2 className="section-title">Powerful Features</h2>
          <p className="section-description">
            Built with modern technologies to provide the best conversational AI
            experience
          </p>
        </div>

        <div className="features-grid">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div key={index} className="feature-card card">
                <div className="feature-icon">
                  <Icon size={32} />
                </div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Capabilities Section */}
      <section className="capabilities-section">
        <div className="capabilities-content">
          <div className="capabilities-text">
            <h2 className="section-title">What Can I Do?</h2>
            <p className="section-description">
              Our chatbot is capable of handling various types of queries and
              tasks with intelligence and precision.
            </p>

            <ul className="capabilities-list">
              {capabilities.map((capability, index) => (
                <li key={index} className="capability-item">
                  <CheckCircle className="check-icon" size={20} />
                  <span>{capability}</span>
                </li>
              ))}
            </ul>

            <Link to="/chat" className="btn btn-primary">
              Try It Now
              <ArrowRight size={18} />
            </Link>
          </div>

          <div className="capabilities-visual">
            <div className="chat-preview">
              <div className="chat-message user-message">What is 15 * 24?</div>
              <div className="chat-message bot-message">
                The result of 15 * 24 is 360
              </div>
              <div className="chat-message user-message">
                Tell me about LangChain
              </div>
              <div className="chat-message bot-message">
                LangChain is a framework for developing applications powered by
                language models...
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-content">
          <h2 className="cta-title">Ready to Get Started?</h2>
          <p className="cta-description">
            Start chatting with our AI assistant and experience intelligent
            conversations
          </p>
          <Link to="/chat" className="btn btn-primary btn-large">
            Launch Chatbot
            <ArrowRight size={20} />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
