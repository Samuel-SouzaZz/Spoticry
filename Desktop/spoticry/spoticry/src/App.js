import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import MusicPage from './pages/MusicPage';
import PlaylistPage from './pages/PlaylistPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import Header from './components/Shared/Header';
import Footer from './components/Shared/Footer';
import PrivateRoute from './components/Shared/PrivateRoute';
import ErrorPage from './pages/ErrorPage';

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<PrivateRoute><HomePage /></PrivateRoute>} />
        <Route path="/music" element={<PrivateRoute><MusicPage /></PrivateRoute>} />
        <Route path="/playlists" element={<PrivateRoute><PlaylistPage /></PrivateRoute>} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
