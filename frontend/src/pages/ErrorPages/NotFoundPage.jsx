import { Link } from "react-router-dom";
import { Home, Search, MessageSquare, ArrowLeft } from "lucide-react";
import "./ErrorPages.css";

const NotFoundPage = () => {
  return (
    <div className="error-page error-404">
      <div className="error-container">
        <div className="error-illustration">
          <div className="error-code">404</div>
          <div className="floating-elements">
            <Search className="float-1" size={40} />
            <MessageSquare className="float-2" size={35} />
            <Home className="float-3" size={30} />
          </div>
        </div>

        <div className="error-content">
          <h1 className="error-title">Page Not Found</h1>
          <p className="error-description">
            Oops! The page you're looking for seems to have wandered off into
            the digital void. Don't worry, even our AI chatbot gets lost
            sometimes!
          </p>

          <div className="error-actions">
            <Link to="/" className="btn btn-primary btn-large">
              <Home size={20} />
              Back to Home
            </Link>
            <Link to="/chat" className="btn btn-secondary btn-large">
              <MessageSquare size={20} />
              Start Chatting
            </Link>
          </div>

          <div className="error-suggestions">
            <p className="suggestions-title">You might want to:</p>
            <ul className="suggestions-list">
              <li>
                <Link to="/">Go to the homepage</Link>
              </li>
              <li>
                <Link to="/chat">Try our chatbot</Link>
              </li>
              <li>
                <Link to="/statistics">View statistics</Link>
              </li>
              <li>
                <button
                  onClick={() => window.history.back()}
                  className="link-button"
                >
                  <ArrowLeft size={16} />
                  Go back to previous page
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage;
