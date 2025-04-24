import React from 'react'
import Title from './Title'
const Latest = () => {

  return (
    <div className='my-10'>
        <div className='text-center py-8 text-3xl'>
             <Title text1={'LATEST'} text2={'COLLECTION'}/>
             <p className='w-3/4 m-auto text-xs sm:text-sm md:text-base text-gray-600'>
             Lorem Ipsum is simply dummy text of the printing and typesetting industry.
             </p>
        </div>
        {/*rendering products*/}
        <div className='grids grid-col-2 sm:grid-col-3 md:grid-col-4 lg:grid-col-5 gap-4 gap-y-6'>

        </div>
    </div>
  )
}

export default Latest