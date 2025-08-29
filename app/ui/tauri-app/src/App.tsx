import "./App.css";
import Aside from "./components/Aside";
import Input from "./components/chat/Input";
function App() {
  
  return (
    <div className="container mx-auto h-screen w-screen mt-6">
      <div className="flex items-end space-x-3">
        <Aside />
        <Input handleSubmit={()=>{}}/>
      </div>
    </div>
  )
}

export default App;
