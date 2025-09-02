
import React from "react"
import { useState } from "react"

type databaseDataType = {
    uri?:string,
    name?:string,
    user?:string,
    password?:string,
    host?:string,
    port?:number
}
const Settings: React.FC = () =>{
    const [ databaseData, setDatabaseData ] = useState<databaseDataType>({})
    const [ obsecure, setObsecure ] = useState(true)
    function onChange(e: React.ChangeEvent<HTMLInputElement>) {
        const { name, value } = e.target;
        setDatabaseData(prev => ({
            ...prev,
            [name]: value, 
        }));
    }
    return (
        <div className="text-white">
            <div className="space-y-3">
                <h2>Database</h2>
                <div className="border border-[#d6d6d620] rounded-md p-3">
                    <div className="space-y-1 flex flex-col">
                        <span className="opacity-70">URI</span>
                        <input onChange={onChange} value={databaseData.uri} name="uri" className="focus:outline-none focus:border-[#d6d6d650] p-2 rounded-md bg-none border-2 border-[#d6d6d610]" />
                    </div>
                    <div className="space-y-1">
                        <div className="flex items-center space-x-1">
                            <div className="space-y-1 flex flex-col w-1/3">
                                <span className="opacity-70">Name</span>
                                <input onChange={onChange} value={databaseData.name} name="name" className="focus:outline-none focus:border-[#d6d6d650] p-2 rounded-md bg-none border-2 border-[#d6d6d610]" />
                            </div>
                            <div className="space-y-1 flex flex-col w-1/3">
                                <span className="opacity-70">User</span>
                                <input onChange={onChange} value={databaseData.user} name="user" className="focus:outline-none focus:border-[#d6d6d650] p-2 rounded-md bg-none border-2 border-[#d6d6d610]" />
                            </div>
                            <div className="space-y-1 flex flex-col w-1/3">
                                <span className="opacity-70">Password</span>
                                <div className="relative">
                                    <input onChange={onChange} value={databaseData.password} type={`${obsecure ? 'password':'text'}`} name="password" className="w-full focus:outline-none focus:border-[#d6d6d650] p-2 rounded-md bg-none border-2 border-[#d6d6d610]" />
                                    <img src={`/icons/eye-${obsecure ? 'closed.svg' : 'opened.svg'}`} className="absolute w-5 cursor-pointer right-1 top-[30%]" onClick={(e)=>{setObsecure(!obsecure)}} />
                                </div>
                            </div>
                        </div>

                    </div>
                    <div className="space-y-1">
                        <div className="flex items-center space-x-1">
                            <div className="space-y-1 flex flex-col w-1/3">
                                <span className="opacity-70">Host</span>
                                <input onChange={onChange} value={databaseData.host} name="host" className="focus:outline-none focus:border-[#d6d6d650] p-2 rounded-md bg-none border-2 border-[#d6d6d610]" />
                            </div>
                            <div className="space-y-1 flex flex-col w-1/3">
                                <span className="opacity-70">PORT</span>
                                <input onChange={onChange} value={databaseData.port} type="number" name="port" className="focus:outline-none focus:border-[#d6d6d650] p-2 rounded-md bg-none border-2 border-[#d6d6d610]" />
                            </div>
                        </div>

                    </div>
                    <button onClick={(e)=>{
                          if (databaseData.uri && databaseData.uri.trim() !== "") {
                                console.log("Safe: URI provided");
                        } else {
                            const { name, user, password, host, port } = databaseData;
                            if (name && user && password && host && port) {
                            console.log("Safe: All fields provided");
                            } else {
                            console.log("Error: Missing required fields");
                            }
                        }}}  
                        className="cursor-pointer p-2 w-[8rem] my-3 bg-blue-700 hover:bg-blue-600 rounded-md text-white" >Save</button>
                </div>
            </div>
        </div>
    )
}

export default Settings


