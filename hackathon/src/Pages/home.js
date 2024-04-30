import React, { useState, useEffect, useRef } from 'react';
import Navbar from '../Components/navbar';
import { refreshData_api } from '../API/api';
import Updating_Chart from '../Components/updating_chart';
import { update_chart } from '../Components/updating_chart';

const Home = () => {
  const [data, setData] = useState(null);
  async function refreshData() {
    refreshData_api()
    .then((result) => {
      setData(result);
    })
  }
  useEffect(() => {
    refreshData();
  }, []);
  
  return(
    <div style={{textAlign: 'center'}}>
      <Navbar />
        <Updating_Chart data={data}/>
      <button onClick={refreshData}> refreshData </button>
    </div>
  )

}

export default Home;