import { HashRouter, Routes, Route } from "react-router-dom";
import ChatArea from "./components/chat/ChatArea";
import IngestMain from "./components/ingest/Main";
import ReportMain from "./components/report/ReportMain";
import Layout from "./Layout";

export default function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path="chatbot" element={<ChatArea />} />
          <Route index element={<ChatArea />} />
          <Route path="ingest" element={<IngestMain />} />
          <Route path="report" element={<ReportMain />} />
        </Route>
      </Routes>
    </HashRouter>
  );
}