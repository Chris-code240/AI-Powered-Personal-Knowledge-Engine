import React from "react";
import { useState } from "react";
type InputProp = {
    handleSubmit: () =>void;
}


const Input: React.FC<InputProp> = ({handleSubmit = ()=>{}}) => {
    const [ inputEmpty, setInputEmpty ] = useState(true)

    function inputChange(e:React.ChangeEvent<HTMLInputElement>){
        e.preventDefault()
        e.target.value.length < 1 ? setInputEmpty(true) : setInputEmpty(false)
    }
    return (
        <form onSubmit={handleSubmit} className="w-full flex items-center">
            <input onChange={inputChange} type="text" className="w-full focus:outline-none bg-[#fafafa] text-md h-[2.5rem] border-[#fafafa60] rounded-l-full px-3 text" />
            <button type="submit" className="cursor-pointer h-[2.5rem] bg-white rounded-r-full flex items-center justify-center p-1">

                <div className={`w-8 h-8 bg-[${inputEmpty ? '#d6d6d6' : '#111111'}] rounded-full flex items-center justify-center`}>
                    <img src={`/icons/arrow-up-${inputEmpty ? 'black': 'white'}.svg`} className="w-5" alt="send" />
                </div>
            </button>
        </form>
    )
}

export default Input