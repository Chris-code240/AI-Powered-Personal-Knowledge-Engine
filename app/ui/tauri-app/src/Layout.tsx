
import React from "react"
import { Outlet } from "react-router-dom"
import Aside from "./components/Aside"
const Layout: React.FC = ()=>{


    return (
    <div className="container mx-auto h-screen w-screen overflow-hidden">

      <div className="flex items-center w-fulll h-[95%] space-x-6 mt-3">
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