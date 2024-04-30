import React from 'react';
import { Link } from "react-router-dom";
import './navbar.css';

function Navbar() {
  // adding the states 
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/make_payment">Make Payments</Link></li>
      </ul>
    </nav>
  );
}
export default Navbar;