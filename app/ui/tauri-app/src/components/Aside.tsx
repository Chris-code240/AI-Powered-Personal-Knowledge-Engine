import { Link } from "react-router-dom";
import AsideLink from "./AsideLink";
import Logo from "./Logo";
export default function Aside(){

    return (
        <aside className="h-full w-full space-y-6">
            <Logo />
            <div className="rounded-md bg-[#42424260] w-full h-[80vh] p-3 flex flex-col justify-between">
                
                <div className="flex flex-col gap-3">
                        <AsideLink label="ChatBot" icon="chat.svg" onClick={()=>{}} path="chat" />
                        <AsideLink label="Ingest" icon="add.svg" onClick={()=>{}} path="ingest" />
                        <AsideLink label="Report" icon="report.svg" onClick={()=>{}} path="report" />
                </div>

                <Link to={"settings"} >
                    <div className="cursor-pointer text-white w-full h-[3rem] rounded-md bg-[#111111] hover:bg-black flex items-center justify-between px-3">
                    <span>Settings</span><img src="/icons/settings.svg" className="w-5" />
                </div>
                </Link>
            </div>
            
        </aside>
    )
}