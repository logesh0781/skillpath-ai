import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import Landing from "./pages/Landing";
import Courses from "./pages/Courses";
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import StudentDashboard from "./pages/student/StudentDashboard";
import InstructorDashboard from "./pages/instructor/InstructorDashboard";
import AdminDashboard from "./pages/admin/AdminDashboard";

export default function App() {
  return (
    <div className="min-h-screen bg-parchment">
      <Navbar />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/dashboard"
          element={<ProtectedRoute roles={["student"]}><StudentDashboard /></ProtectedRoute>}
        />
        <Route
          path="/instructor"
          element={<ProtectedRoute roles={["instructor", "super_admin"]}><InstructorDashboard /></ProtectedRoute>}
        />
        <Route
          path="/admin"
          element={<ProtectedRoute roles={["super_admin"]}><AdminDashboard /></ProtectedRoute>}
        />
      </Routes>
    </div>
  );
}
