import { Routes,Route } from "react-router-dom"
import React from 'react'
import Login from "./pages/Login"
import Collection from "./pages/Collection"
import Product from "./pages/Product"
import Order from "./pages/Order"
import PlaceOrder from "./pages/PlaceOrder"
import About from "./pages/About"
import Contact from "./pages/Contact"
import Cart from "./pages/Cart"
import Home from "./pages/Home"
import Navbar from "./components/Navbar"


function App() {

  return (
    <div className="px-4 sm:px-[5vw] md:px-[7vw] lg:px-[9vw]">
      <Navbar/>
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/collection" element={<Collection/>}/>
        <Route path="/About" element={<About/>}/>
        <Route path="/contact" element={<Contact/>}/>
        <Route path="/product/:ProductId" element={<Product/>}/>
        <Route path="/cart" element={<Cart/>}/>
        <Route path="/order" element={<Order/>}/>
        <Route path="/placeorder" element={<PlaceOrder/>}/>
      </Routes>
    </div>
  )
}

export default App
