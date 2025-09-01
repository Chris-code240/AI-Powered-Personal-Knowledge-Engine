import AsideLink from "./AsideLink";
import { Link } from "react-router-dom";
export default function Aside(){

    return (
        <aside className="h-full w-full space-y-6">
            <div className="logo w-full h-[3rem] rounded-md bg-[#42424260] text-white flex items-center space-x-3 px-3">
                <img src="/icons/data.svg" className="w-7" /><span>Knowledge Engine</span>
                
            </div>
            <div className="rounded-md bg-[#42424260] w-full h-[80vh] p-3 flex flex-col justify-between">
                
                <div className="space-y-6">
                    <Link to={"chatbot"} >
                        <AsideLink label="ChatBot" icon="chat.svg" onClick={()=>{}} />
                    </Link>
                    <Link to={"ingest"}>
                        <AsideLink label="Ingest" icon="add.svg" onClick={()=>{}} />
                    </Link>
                    <Link to={"report"}>
                        <AsideLink label="Report" icon="report.svg" onClick={()=>{}} />
                    </Link>
                </div>

                <div className="cursor-pointer text-white w-full h-[3rem] rounded-md bg-[#111111] hover:bg-black flex items-center justify-between px-3">
                    <span>Settings</span><img src="/icons/settings.svg" className="w-5" />
                </div>
            </div>
            
        </aside>
    )
}