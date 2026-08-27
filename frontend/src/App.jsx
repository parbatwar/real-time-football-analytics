import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import LiveMatchPage from "./pages/LiveMatchPage";
import HistoryPage from "./pages/HistoryPage";
import MatchDetailsPage from "./pages/MatchDetailsPage";

import "./App.css";


function App() {
  return (
    <BrowserRouter>

      <Navbar />

      <Routes>

        <Route
          path="/"
          element={<LiveMatchPage />}
        />

        <Route
          path="/history"
          element={<HistoryPage />}
        />

        <Route
          path="/history/:matchId"
          element={<MatchDetailsPage />}
        />

      </Routes>

    </BrowserRouter>
  );
}


export default App;