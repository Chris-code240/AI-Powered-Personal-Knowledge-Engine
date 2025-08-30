import "./App.css";
import IngestMain from "./components/ingest/Main";
import Aside from "./components/Aside";
function App() {
  
  return (
    <div className="container mx-auto h-screen w-screen pt-3 pb-3">

        <div className="flex items-center w-full h-full justify-between">
          <div className="w-[18%] h-full">
            <Aside />
          </div>
          <div className="w-[80%] h-full">
            <IngestMain />
          </div>
        </div>

    </div>
  )
}

export default App;
