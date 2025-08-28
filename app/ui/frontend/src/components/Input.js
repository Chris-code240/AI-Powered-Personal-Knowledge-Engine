import { useState } from "react"
export default function Input(){
    const [ inputChange, setInputChange ] = useState(false)

    function handleOnChange(e){

        e.target.value.length > 0 ? setInputChange(true) : setInputChange(false)
    }

    return (
        <form className="relative w-full flex items-center">
           <button className="absolute left-[5px] py-2 px-3 rounded-full w-[2rem] h-[2rem] md:w-[3rem] md:h-[3rem] p-1.5 flex items-center justify-center text-2xl md:text-3xl">+</button> 
           <input type="text" onChange={handleOnChange}  className="placeholder:text-gray-500 px-[2.5rem] md:text-xl focus:outline-none border-none w-full px-3 py-2 md:py-3 rounded-full" placeholder="What can I help you with?" />
            <span className={`absolute right-[5px] w-[2rem] h-[2rem] md:w-[2.5rem] md:h-[2.5rem]  ${inputChange ? 'bg-black':'bg-[#d6d6d660]'} p-1.5 rounded-full`}>
                    <img src="/icons/arrow-up.svg" alt="send" className="w-full h-full" />
                </span>
        </form>
    )
}