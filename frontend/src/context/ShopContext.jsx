import { createContext } from "react"

export const ShopContext = createContext()

const ShopContextProvider = (props)=>{
    const currency ='$'
    const ShippingFee=10

    const values ={
        currency,ShippingFee
     }
    return(
       <ShopContext.Provider value={values}>
            {props.children}
       </ShopContext.Provider>
    )
}

export default ShopContextProvider