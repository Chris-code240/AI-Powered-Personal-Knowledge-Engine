import React from "react";

type AsideLinkProp = {
  label: string;
  icon:string;
  onClick: () => void;
  disabled?: boolean;
};
const AsideLink: React.FC<AsideLinkProp> = ({label, icon, onClick, disabled=false}) =>{

    return (
        <button onClick={onClick} disabled={disabled} className="cursor-pointer text-white font-thin w-full h-[2.5rem] rounded-md bg-[#42424280] hover:bg-transparent hover:border-[#d6d6d640] border border-transparent flex items-center justify-between px-3">
            <span>{label}</span><img src={`/icons/${icon.toLowerCase()}`} className="w-5" />
        </button>
    )
}

export default AsideLink;