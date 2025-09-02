import "./App.css";
import ChatArea from "./components/chat/ChatArea";
import IngestMain from "./components/ingest/Main";
import ReportMain from "./components/report/ReportMain";
import Settings from "./components/Settings";
import { HashRouter, Route, Routes } from "react-router-dom";
import Layout from "./Layout";
function App() {
  
  return (
      <HashRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route path="chat" element={<ChatArea />}  />
            <Route index element={<ChatArea />}  />
            <Route path="chatbot" element={<ChatArea />}  />
            <Route path="ingest" element={<IngestMain />}  />
            <Route path="report" element={<ReportMain />}  />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
      </HashRouter>
  )
}

export default App;
