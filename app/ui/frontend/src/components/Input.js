import { useState } from "react"
export default function Input({addChat = ()=>{}}){
    const [ inputChange, setInputChange ] = useState(false)
    const [ query, setQuery ] = useState("")

    function handleOnChange(e){
        e.target.value.length > 0 ? setInputChange(true) : setInputChange(false)
        setQuery(e.target.value)
    }
    function handleSubmit(e){
        e.preventDefault()
        addChat({"text":query, "type":"user-input"})
    }
    return (
        <form className="relative w-full flex items-center" onSubmit={handleSubmit}>
           <input type="text" onChange={handleOnChange}  className="shadow-md placeholder:text-gray-500 px-[2.5rem] md:text-xl focus:outline-none border-none w-full pr-3 py-2 md:py-3 rounded-full" placeholder="What can I help you with?" />
            <button type="submit" className="absolute right-[7px] p-0 w-[2rem] h-[2rem] md:w-[2.2rem] md:h-[2.2rem] flex items-center justify-center">
                <span className={`w-full h-full   ${inputChange ? 'bg-black':'bg-[#d6d6d6]'} p-1 rounded-full`}>
                    <img src="/icons/arrow-up.svg" alt="send" className="w-full h-full" />
            </span>
            </button>
        </form>
    )
}