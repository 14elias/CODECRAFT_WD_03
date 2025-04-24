import React from 'react'
import { useState } from 'react';
import { Link, NavLink } from 'react-router-dom'
import { CiSearch } from "react-icons/ci";
import { FaUser } from 'react-icons/fa';
import { FaBars } from 'react-icons/fa';
import { FaShoppingCart } from 'react-icons/fa';

const Navbar = () => {
    const [visible,setVisible] = useState(false)

    const handleClick = ()=>{
        setVisible(!visible)
    }

  return (
    <div className='flex items-center justify-between py-5 font-medium'>
        <p className='w-36'>MyEcom</p>

        <ul className='hidden sm:flex gap-5 text-sm text-gray-700'>
            <NavLink to='/' className='flex flex-col items-center gap-1'>
                <p>Home</p>
                <hr className='w-2/4 border-home h-[1.5px] bg-gray-700 hidden'/>
            </NavLink>
            <NavLink to='/collection' className='flex flex-col items-center gap-1'>
                <p>Collection</p>
                <hr className='w-2/4 border-home h-[1.5px] bg-gray-700 hidden'/>
            </NavLink>
            <NavLink to='/about' className='flex flex-col items-center gap-1'>
                <p>About</p>
                <hr className='w-2/4 border-home h-[1.5px] bg-gray-700 hidden'/>
            </NavLink>
            <NavLink to='/contact' className='flex flex-col items-center gap-1'>
                <p>Contact</p>
                <hr className='w-2/4 border-home h-[1.5px] bg-gray-700 hidden'/>
            </NavLink>

        </ul>
        <div className='flex items-center gap-6'>
            <CiSearch className='w-5 cursor-pointer'/>
            <div className='group relatives'>
                <FaUser className='w-5 cursor-pointer'/>
                <div className='group-hover:block hidden absolute dropdown-menu right-0 pt-4'>
                    <div className='flex flex-col gap-2 w-36 py-3 px-5 bg-slate-100 text-gray-500 rounded'>
                        <p className='cursor-pointer hover:text-black'>My Profile</p>
                        <p className='cursor-pointer hover:text-black'>Orders</p>
                        <p className='cursor-pointer hover:text-black'>Logout</p>

                    </div>

                </div>

            </div>
            <Link to='/cart' className='relative'>
                <FaShoppingCart className='w-5 min-w-5'/>
                <p className='absolute right-[-5px] bottom-[-5px] w-4 text-center leading-4 bg-black text-white aspect-square rounded-full text-[8px]'>10</p>
            </Link>
            <FaBars className='w-5 cursor-pointer sm:hidden' onClick={handleClick}/>
        </div>
        {/* side bar menu for small screens */}
        <div className={`absolute top-0 right-0 bottom-0 overflow-hidden bg-white transition-all ${visible? 'w-full':'w-0'}`}>
            <div className='flex flex-col text-gray-600'>
                <div className='flex item-center gap-4 p-3 cursor-pointer' onClick={handleClick}>
                    <p>Back</p>
                </div>
                <NavLink to='/' className='py-2 pi-6 border' onClick={handleClick}>Home</NavLink>
                <NavLink to='/collection' className='py-2 pi-6 border' onClick={handleClick}>Collection</NavLink>
                <NavLink to='/about' className='py-2 pi-6 border' onClick={handleClick}>About</NavLink>
                <NavLink to='/contact' className='py-2 pi-6 border' onClick={handleClick}>Contact</NavLink>

            </div>

        </div>
    </div>
  )
}

export default Navbar