import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import AddCryptoPage from "./pages/AddCryptoPage";
import { isAuthenticated } from "./utils/auth";

const ProtectedRoute = ({ element }) =>
  isAuthenticated() ? element : <Navigate to="/login" />;

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/add-crypto" element={<AddCryptoPage />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
