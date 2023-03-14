import Cloud from "../img/cloud.png"
import { NavLink } from "react-router-dom"

const Nav = () => (
  <header className="nav-bar">
    <img className="logo" src={Cloud} alt="a logo shaped like a cloud"/>
    <nav className="navigation">
      <ul className="nav-links">
        <li><NavLink to="/">home</NavLink></li>
        <li><NavLink to="/contact">contact</NavLink></li>
        <li><NavLink to="/about">about</NavLink></li>
        <li><NavLink to="/profile">profile</NavLink></li>
      </ul>
    </nav>
  </header>
)


export default Nav