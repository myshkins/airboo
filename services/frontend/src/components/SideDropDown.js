import { BiChevronDown } from "react-icons/bi"
import HomeButton from "./HomeButton"


const SideDropDown = (props) => {
  return (
    <div className="dropdown-wrap">
      <div className="dropdown-btn" onClick={props.onClick}>
        {props.name} <BiChevronDown />
      </div>
      <div className="dropdown">
        {props.contentVisible ?
          <>
            {props.children}
          </> : null}
      </div>
    </div>
  )
}
export default SideDropDown