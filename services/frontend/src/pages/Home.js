import HomeSideBarLeft from "../components/HomeSideBarLeft";
import HomeSideBarRight from "../components/HomeSideBarRight";
import HomeGraph from "../components/HomeGraph";
import "./Home.css";
import SideDropDown from "../components/SideDropDown";
import SideDropDownCheckbox from "../components/SideDropDownCheckbox";
import SideDropDownRadio from "../components/SideDropDownRadio";
import EditStationsWindow from "../components/EditStationsWindow";
import React, { useEffect, useState } from "react";
import HomeButton from "../components/HomeButton";
import { config } from "../Constants";

const Home = () => {
  const timePeriods = [
    "6hr",
    "12hr",
    "24hr",
    "48hr",
    "5day",
    "10day",
    "1month",
  ];
  const [stations, setStations] = useState([]);
  const [tempStations, setTempStations] = useState(null);
  const [leftSideBarVisible, setLeftSideBarVisible] = useState(true);
  const [stationDropVisible, setStationDropVisible] = useState(true);
  const [editStationPopupVisible, setEditStationPopupVisible] = useState(false);
  const [timeDropVisible, setTimeDropVisible] = useState(true);
  const [zipcode, setZipcode] = useState("11206");
  const [zipQuery, setZipQuery] = useState("11206");
  const [airData, setAirData] = useState({});

  const toggleSideBar = () => {
    setLeftSideBarVisible(!leftSideBarVisible);
  };

  const toggleStationDrop = () => {
    setStationDropVisible(!stationDropVisible);
  };

  const toggleTimeDrop = () => {
    setTimeDropVisible(!timeDropVisible);
  };

  const toggleEditStationPopup = () => {
    setEditStationPopupVisible(!editStationPopupVisible);
  };

  const handleZipcodeChange = (e) => {
    setZipcode(e.target.value);
  };

  const handleZipQueryChange = () => {
    setZipQuery(zipcode);
  };

  const getReadings = () => {};

  const updateStations = (e) => {
    e.preventDefault();
    let trueStations = tempStations.map((station) =>
      station["checked"] === true
        ? {
            station_id: station["station_id"],
            station_name: station["station_name"],
            latitude: station["latitude"],
            longitude: station["longitude"],
            location_coord: station["location_coord"],
          }
        : null
    );
    let newStations = trueStations.filter(Boolean);
    setStations(newStations);
    toggleEditStationPopup();
  };

  const handleCheckChange = (e) => {
    let updatedTempStations = tempStations.map((station) =>
      station["station_id"] === e.target.name
        ? {
            station_id: station["station_id"],
            station_name: station["station_name"],
            latitude: station["latitude"],
            longitude: station["longitude"],
            location_coord: station["location_coord"],
            checked: !station["checked"],
          }
        : station
    );
    setTempStations(updatedTempStations);
  };

  useEffect(() => {
    const findStations = async () => {
      const response = await fetch(
        `${config.urls.STATIONS_URL}${zipcode}`,
        { mode: "cors" }
      );

      const data = await response.json();
      const tempArr = [...data, ...stations];
      const tempArrTwo = tempArr.filter(
        (value, index, arr) =>
          index ===
          arr.findIndex((item) => item["station_id"] === value["station_id"])
      );
      tempArrTwo.forEach((station) => (station["checked"] = false));

      setTempStations(tempArrTwo);
    };

    findStations();
  }, [zipQuery]);

  useEffect(() => {
    const getAirData = async () => {
      const response = await fetch(``);
    };
  });
  return (
    <div className="dashboard-container">
      <HomeSideBarLeft
        toggleSideBar={toggleSideBar}
        contentVisible={leftSideBarVisible}
      >
        {editStationPopupVisible ? (
          <EditStationsWindow
            zipcode={zipcode}
            setZipcode={setZipcode}
            tempStations={tempStations}
            updateStations={updateStations}
            handleCheckChange={handleCheckChange}
            handleZipcodeChange={handleZipcodeChange}
            handleZipQueryChange={handleZipQueryChange}
          />
        ) : null}
        <SideDropDown
          name={"stations"}
          onClick={toggleStationDrop}
          contentVisible={stationDropVisible}
        >
          {stations.map((station) => (
            <SideDropDownCheckbox
              key={station["station_id"]}
              name={station["station_id"]}
              value={station["station_name"]}
              checked={station["checked"]}
            />
          ))}
          <HomeButton
            onClick={toggleEditStationPopup}
            value={"add/remove stations"}
          />
        </SideDropDown>

        <SideDropDown
          name={"time period"}
          onClick={toggleTimeDrop}
          contentVisible={timeDropVisible}
          hasBtn={false}
        >
          {timePeriods.map((period) => (
            <SideDropDownRadio
              key={period}
              name={period}
              value={period}
              type="radio"
            />
          ))}
        </SideDropDown>
        <HomeButton onClick={getReadings} value={"update graph"} />
      </HomeSideBarLeft>

      <HomeGraph />

      <HomeSideBarRight />
    </div>
  );
};

export default Home;
