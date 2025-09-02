import React from "react";
import { useState } from "react";
type InputProp = {
    handleSubmit: (e:React.FormEvent<HTMLFormElement>) =>void;
    setQuery: React.Dispatch<React.SetStateAction<string>>
    query:string | undefined 
}



const Input: React.FC<InputProp> = ({query,setQuery, handleSubmit}) => {
    const [ inputEmpty, setInputEmpty ] = useState(true)
    function inputChange(e:React.ChangeEvent<HTMLInputElement>){
        const value = e.target.value
        value.length < 1 ? setInputEmpty(true) : setInputEmpty(false)
        setQuery(value)
    }
    return (
        <form onSubmit={(e: React.FormEvent<HTMLFormElement>)=>{
            handleSubmit(e)
            setQuery('')
            setInputEmpty(true)
        }} className="flex items-center">
            <input onChange={inputChange} value={query} type="text" className="w-full focus:outline-none bg-[#fafafa] text-md h-[2.5rem] border-[#fafafa60] rounded-l-full px-3 text" />
            <button type="submit" className="cursor-pointer h-[2.5rem] bg-white rounded-r-full flex items-center justify-center p-1">

                <div className={`w-8 h-8 bg-[${inputEmpty ? 'gray-400' : '#111111'}] rounded-full flex items-center justify-center`}>
                    <img src={`/icons/arrow-up-${inputEmpty ? 'black': 'white'}.svg`} className="w-5" alt="send" />
                </div>
            </button>
        </form>
    )
}

export default Input