import HomeSideBarLeft from "../components/HomeSideBarLeft";
import HomeSideBarRight from "../components/HomeSideBarRight"
import HomeGraph from "../components/HomeGraph"
import "./Home.css"
import SideDropDown from "../components/SideDropDown";
import SideDropDownInput from "../components/SideDropDownInput";

const Home = (props) => {
  const timePeriods = ["6hr", "12hr", "24hr", "48hr", "5day", "10day", "1month"]

  return (
    <div className="dashboard-container">
      <HomeSideBarLeft
        toggleSideBar={props.toggleSideBar}
        contentVisible={props.leftSideBarVisible}>

        <SideDropDown
          name={"stations"} 
          onClick={props.toggleStationDrop}
          contentVisible={props.stationDropVisible}>
          {props.stations.map((station) => (
            <SideDropDownInput
              key={station}
              name={station.split(" ")[0]}
              value={station}
              type="checkbox" />
          ))}
        </SideDropDown>

        <SideDropDown
          name={"time period"}
          onClick={props.toggleTimeDrop}
          contentVisible={props.timeDropVisible}>
          {timePeriods.map((period) => (
            <SideDropDownInput
              key={period}
              name={period}
              value={period}
              type="radio" />
          ))}
        </SideDropDown>

      </HomeSideBarLeft>

      <HomeGraph />

      <HomeSideBarRight />
    </div>
  )
};

export default Home;