import React from "react";
import { Link } from "react-router-dom";

type AsideLinkProp = {
  label: string;
  icon:string;
  onClick: () => void;
  disabled?: boolean;
  path:string
};
const AsideLink: React.FC<AsideLinkProp> = ({label, icon, onClick, disabled=false,path }) =>{

    return (
        <Link to={path} >
            <button onClick={onClick} disabled={disabled} className="cursor-pointer text-white font-thin w-full h-[2.5rem] rounded-md bg-[#42424280] hover:bg-transparent hover:border-[#d6d6d640] border border-transparent flex items-center justify-between px-3">
            <span>{label}</span><img src={`/icons/${icon.toLowerCase()}`} className="w-5" />
        </button>
        </Link>
    )
}

export default AsideLink;