import { useState } from 'react';
import './App.css';
import Logo from './components/Logo';
import Input from './components/Input';
import Chat from './components/Chat';

function App() {
  const response = { text: "A bunch of text", sources: ["https://geekforgeeks.com/python/variables"], type: "response" }
  const chat = { text: "A bunch of text", type: "user-input" }
  const [chats, setChats] = useState([response, chat])
  function addChat(chat){
    let c = [...chats, chat]
    setChats(c)
  }
  return (
    <div className='h-screen w-screen'>
      <div className='relative container mx-auto md:px-6 md:w-[70%] w-[90%] h-full overflow-hidden'>
        <div className='absolute w-full bg-white'>
            <div className=' top-0 cursor-pointer flex items-center space-x-1 hover:bg-[#f1f1f1] w-[11rem] rounded-md'>
            <Logo />
            <span>Knowledge Engine</span>
            </div>
        </div>
        <main className='absolute top-6 w-full overflow-scroll mt-6 h-[80vh]'>
          <Chat chats = {chats} />

        </main>
        <div className='absolute bottom-0 w-full h-[5rem] bg-white'>
          <Input addChat = {addChat} />
        </div>

      </div>
    </div>
  );
}

export default App;
