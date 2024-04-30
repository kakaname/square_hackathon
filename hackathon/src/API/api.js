import React, {useEffect, useState} from 'react';

const urlBase = "http://localhost:5000";

export async function get_hello() {
  try {
    const response = await fetch(`${urlBase}/get_hello`);
    const journalsJSON = await response.json();
    return journalsJSON;
  } catch (error) {
    console.log("Error:", error);
    return [];
  }
}

export async function make_payment_api(value, service){
  const apiUrl = `${urlBase}/make_payment`;
  try {
    const sendData = {
      value : value,
      service : service
    }
    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type' : 'application/json'
      },
      body: JSON.stringify(sendData),
    })
    .then(response => {
      response = response;
    })
    .catch((error) => {
      console.error('Error:', error);
    })

  } catch (error) {
    console.log("Error:", error);
  }
}


export async function refreshData_api(){
  return fetch(`${urlBase}/fetch_all_data`, 
  {
    method : 'GET',
    headers : {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  })
  .then((response) => response.json())
  .then((responseData) => {return responseData})
  .catch((error) => {
    console.error('Error:', error);
  })


}