import HomeSideBarLeft from "../components/HomeSideBarLeft";
import HomeSideBarRight from "../components/HomeSideBarRight"
import HomeGraph from "../components/HomeGraph"
import "./Home.css"
import SideDropDown from "../components/SideDropDown";
import SideDropDownInput from "../components/SideDropDownInput";
import EditStationsWindow from "../components/EditStationsWindow";
import React, { useEffect, useState } from 'react';


const Home = (props) => {
  const timePeriods = ["6hr", "12hr", "24hr", "48hr", "5day", "10day", "1month"]
  const [stations, setStations] = useState(["Brooklyn, NY", "Queens, NY", "Jersey City, NJ"])
  const [leftSideBarVisible, setLeftSideBarVisible] = useState(true)
  const [stationDropVisible, setStationDropVisible] = useState(true)
  const [timeDropVisible, setTimeDropVisible] = useState(true)
  const [zipcode, setZipcode] = useState(11206)

  const toggleSideBar = () => {
    setLeftSideBarVisible(!leftSideBarVisible)
  }

  const toggleStationDrop = () => {
    setStationDropVisible(!stationDropVisible)
  }

  const toggleTimeDrop = () => {
    setTimeDropVisible(!timeDropVisible)
  }

  useEffect (() => {
    findStations()
  }, [])
  
  async function findStations() {
    const response = await fetch(
      `http://localhost:8100/stations/all-nearby/?zipcode=${zipcode}`, {mode: 'cors'}
      )
    const data = await response.json()
    console.log(data[0])
    setStations(data)
    console.log(stations)
  }

 return (
    <div className="dashboard-container">
      <HomeSideBarLeft
        toggleSideBar={toggleSideBar}
        contentVisible={leftSideBarVisible}>
        
        <EditStationsWindow
          zipcode={zipcode}
          setZipcode={setZipcode}
          findStations={findStations} />
        <SideDropDown
          name={"stations"} 
          onClick={toggleStationDrop}
          contentVisible={stationDropVisible}>
          {stations.map((station) => (
            <SideDropDownInput
              key={station["station_id"]}
              name={station["station_id"]}
              value={station["station_name"]}
              type="checkbox" />
          ))}
        </SideDropDown>

        <SideDropDown
          name={"time period"}
          onClick={toggleTimeDrop}
          contentVisible={timeDropVisible}>
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