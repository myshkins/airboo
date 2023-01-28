import { BiChevronLeft } from "react-icons/bi"


const HomeSideBarLeft = (props) => {
  return (
    <div className="left-side-bar">
      <div className="left-chevron-btn">
        <BiChevronLeft onClick={props.toggleSideBar} size={"2rem"} />
      </div>
      {props.contentVisible ?
        <>
          {props.children}
        </> : null}
    </div>
  )
}

export default HomeSideBarLeft