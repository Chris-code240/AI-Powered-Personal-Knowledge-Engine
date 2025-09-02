import React from "react"
import { Link } from "react-router-dom"
const Logo: React.FC = ()=>{

    return (
        <div className="w-full">

            <Link to={"/"} className="w-full" >
            <div className="logo w-full h-[3rem] rounded-md bg-[#42424260] text-white flex items-center space-x-3  p-3">
                <img src="/icons/stack-white.svg" className="w-7" /><span>Knowledge Engine</span>
                
            </div>
        </Link>
        </div>
    )
}

export default Logo