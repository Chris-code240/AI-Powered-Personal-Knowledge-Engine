import React from "react";
import { useState } from "react";
type InputProp = {
    query:string
    setQuery: React.Dispatch<React.SetStateAction<string>>
    bubbles: any[];
    setBubbles:React.Dispatch<React.SetStateAction<any[]>>
}


const Input: React.FC<InputProp> = ({query, setQuery,bubbles,setBubbles}) => {
    const [ inputEmpty, setInputEmpty ] = useState(true)

    function inputChange(e:React.ChangeEvent<HTMLInputElement>){
        e.preventDefault()
        e.target.value.length < 1 ? setInputEmpty(true) : setInputEmpty(false)
        setQuery(e.target.value)
    }
    function handleSubmit(e:React.FormEvent<HTMLFormElement>){
        e.preventDefault()
        if (query.length > 0 ){   
            setInputEmpty(true) 
            let oldBubbles = bubbles
            oldBubbles.push({"text":query, "type":"user-input"})
            oldBubbles.push({"text":`You said: ${query}`, type:"response", "sources":["https://google.com", "https://google.com", "https://google.com"]})
            setBubbles(oldBubbles)
            setQuery("")
        }
    }
    return (
        <form onSubmit={handleSubmit} className="w-full flex items-center">
            <input value={query} onChange={inputChange} type="text" className="w-full focus:outline-none bg-[#fafafa] text-md h-[2.5rem] border-[#fafafa60] rounded-l-full px-3 text" />
            <button type="submit" className="cursor-pointer h-[2.5rem] bg-white rounded-r-full flex items-center justify-center p-1">

                <div className={`w-8 h-8 bg-[${inputEmpty ? '#d6d6d6' : '#111111'}] rounded-full flex items-center justify-center`}>
                    <img src={`/icons/arrow-up-${inputEmpty ? 'black': 'white'}.svg`} className="w-5" alt="send" />
                </div>
            </button>
        </form>
    )
}

export default Input