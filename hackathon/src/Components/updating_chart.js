import React, { useState, useEffect, useRef } from 'react';
import Chart from "chart.js/auto";

const Updating_Chart = ({data}) => {

  const chartRef = useRef(null);

  useEffect(() => {
    var modified_data;
    if (data == null) {
      modified_data = [];
    }else {
      modified_data = data.payments;
    }
    const myChart = new Chart(
      document.getElementById("myChart"),
      {
        type: 'bar',
        data: {
          labels: modified_data.map(row => row.giftcard),
          datasets: [
            {
              label: 'Acquisitions by year',
              data: modified_data.map(row => row.total)
            }
          ]
        }
      });   
    chartRef.current = myChart;
    return () => {
      if(chartRef.current) {
        chartRef.current.destroy();
      }
    }
    }, [data]);

  


  return(
    <div style={{textAlign: 'center'}}>
      <div className="chartContainer">
        <canvas id="myChart" ref={chartRef} />
      </div>
    </div>
  )

}

export default Updating_Chart;