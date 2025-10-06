import { MessageSquare, Heart, Github, Linkedin, Twitter } from "lucide-react";
import "./Footer.css";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        {/* Footer Top */}
        <div className="footer-top">
          <div className="footer-brand">
            <div className="footer-logo">
              <MessageSquare className="footer-logo-icon" />
              <span className="footer-logo-text">Smart Chatbot</span>
            </div>
            <p className="footer-description">
              An intelligent AI-powered chatbot built with LangChain, LangGraph,
              and OpenAI GPT-3.5-turbo. Experience conversational AI at its
              best.
            </p>
          </div>

          <div className="footer-links">
            <div className="footer-section">
              <h3 className="footer-section-title">Product</h3>
              <ul className="footer-list">
                <li>
                  <a href="/chat">Chat</a>
                </li>
                <li>
                  <a href="/history">History</a>
                </li>
                <li>
                  <a href="/statistics">Statistics</a>
                </li>
              </ul>
            </div>

            <div className="footer-section">
              <h3 className="footer-section-title">Resources</h3>
              <ul className="footer-list">
                <li>
                  <a href="#documentation">Documentation</a>
                </li>
                <li>
                  <a href="#api">API Reference</a>
                </li>
                <li>
                  <a href="#support">Support</a>
                </li>
              </ul>
            </div>

            <div className="footer-section">
              <h3 className="footer-section-title">Company</h3>
              <ul className="footer-list">
                <li>
                  <a href="#about">About</a>
                </li>
                <li>
                  <a href="#blog">Blog</a>
                </li>
                <li>
                  <a href="#careers">Careers</a>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="footer-bottom">
          <div className="footer-copyright">
            <span>© {currentYear} Smart Chatbot. Built with</span>
            <Heart size={16} className="heart-icon" />
            <span>using LangChain & LangGraph</span>
          </div>

          <div className="footer-social">
            <a href="#github" className="social-link" aria-label="GitHub">
              <Github size={20} />
            </a>
            <a href="#linkedin" className="social-link" aria-label="LinkedIn">
              <Linkedin size={20} />
            </a>
            <a href="#twitter" className="social-link" aria-label="Twitter">
              <Twitter size={20} />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
