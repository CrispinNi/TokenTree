import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";
import AddCryptoPage from "./pages/AddCryptoPage";
import LandingPage from "./pages/LandingPage";
import { isAuthenticated } from "./utils/auth";

const ProtectedRoute = ({ element }) =>
  isAuthenticated() ? element : <Navigate to="/login" />;

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/dashboard"
            element={<ProtectedRoute element={<DashboardPage />} />}
          />
          <Route
            path="/add-crypto"
            element={<ProtectedRoute element={<AddCryptoPage />} />}
          />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
