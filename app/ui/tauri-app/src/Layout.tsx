import React from "react";
import Aside from "./components/Aside";
import { Outlet } from "react-router-dom";

const Layout: React.FC = ()=> {

    return (
    <div className="container mx-auto h-screen w-screen pt-3 pb-3">

        <div className="flex items-center w-full h-full justify-between">
          <div className="w-[18%] h-full">
            <Aside />
          </div>
          <div className="w-[80%] h-full">
            <Outlet />
          </div>
        </div>

    </div>
    )
}

export default Layout


