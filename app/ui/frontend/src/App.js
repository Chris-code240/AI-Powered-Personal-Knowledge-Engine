import './App.css';
import Logo from './components/Logo';
import Input from './components/Input';
function App() {
  return (
    <div className='bg-[#fafafa] h-screen w-screen'>
      <div className='container mx-auto md:px-6 w-[90%] h-full'>
        <div className='cursor-pointer flex items-center space-x-1 hover:bg-[#f1f1f1] w-[11rem] rounded-md'>
          <Logo />
          <span>Knowledge Engine</span>
        </div>
        <main className=' h-[80%] w-full border-red-400'>

        </main>
        <div className=''>
          <Input />
        </div>

      </div>
    </div>
  );
}

export default App;
