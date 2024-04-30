import { useState } from 'react';
import { get_hello, make_payment_api } from '../API/api.js';
import Navbar from '../Components/navbar.js';

function isInt(value) {
  return !isNaN(value) && 
          parseInt(Number(value)) == value && 
          !isNaN(parseInt(value, 10));
}

const Make_payment = () => {
  const [value, setValue] = useState(20);
  const [service, setService] = useState(80);

  const handleValueChange = (event) => {
    setValue(event.target.value);
  };
  const handleServiceChange = (event) => {
    setService(event.target.value);
  };

  function make_payment_call() {
    if(!isInt(value)){
      alert("please enter a valid value");
    }else if(!isInt(service)) {
      alert("please enter a valid value for service");
    }else{
      make_payment_api(value*100, service*100);
    }
    
  }
  return (
    <div style={{textAlign: 'center'}}>
      <Navbar />
      <p> Cost of Service </p>
      <input type="text" value={service} onChange={handleServiceChange} />
      <p> Value of Giftcard </p>
      <input type="text" value={value} onChange={handleValueChange} />
      <button onClick={make_payment_call}> make payment </button>
    </div>
  );
}

export default Make_payment;
