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
  const [timePeriods, setTimePeriod] = useState({
    "6hr": true,
    "12hr": false,
    "24hr": false,
    "48hr": false,
    "5day": false,
    "10day": false,
    "1month": false,
  });
  const [stations, setStations] = useState([]);
  const [tempStations, setTempStations] = useState(null);
  const [leftSideBarVisible, setLeftSideBarVisible] = useState(true);
  const [stationDropVisible, setStationDropVisible] = useState(true);
  const [editStationPopupVisible, setEditStationPopupVisible] = useState(false);
  const [timeDropVisible, setTimeDropVisible] = useState(true);
  const [zipcode, setZipcode] = useState("11206");
  const [zipQuery, setZipQuery] = useState("11206");
  const [rawData, setRawData] = useState({});
  const [dates, setDates] = useState([]);
  const [aqiData, setAqiData] = useState([]);
  const [idsToGraph, setIdsToGraph] = useState([]);

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

  const pickTimePeriod = (e) => {
    const newPeriods = {};
    for (const key of Object.keys(timePeriods)) {
      key === e.target.name
        ? (newPeriods[key] = true)
        : (newPeriods[key] = false);
    }
    setTimePeriod(newPeriods);
  };

  const updateStations = (e) => {
    e.preventDefault();
    const trueStations = tempStations.map((station) =>
      station["checked"] === true
        ? {
            station_id: station["station_id"],
            station_name: station["station_name"],
            checked: true,
            latitude: station["latitude"],
            longitude: station["longitude"],
            location_coord: station["location_coord"],
          }
        : null
    );
    const newStations = trueStations.filter(Boolean);
    setStations(newStations);
    toggleEditStationPopup();
  };

  const updateIds = () => {
    const newIds = [];
    stations.forEach((station) => {
      if (station["checked"]) {
        newIds.push(station["station_id"]);
      }
    });
    setIdsToGraph(newIds);
  };

  const handleStationCheckChange = (e) => {
    const updatedStations = [...stations];
    updatedStations.forEach((station) => {
      if (station["station_id"] === e.target.name) {
        station["checked"] = !station["checked"];
      }
    });
    setStations(updatedStations);
  };

  const handleTempCheckChange = (e) => {
    const updatedTempStations = [...tempStations];
    updatedTempStations.forEach((station) => {
      if (station["station_id"] === e.target.name) {
        station["checked"] = !station["checked"];
      }
    });
    setTempStations(updatedTempStations);
  };

  useEffect(() => {
    const findStations = async () => {
      const response = await fetch(`${config.urls.STATIONS_URL}${zipcode}`, {
        mode: "cors",
      });

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
    const getReadings = async () => {
      let qParam = idsToGraph.reduce((prev, id) => (prev + `ids=${id}&`), "?");
      if (qParam.slice(-1) === "&") {qParam = qParam.slice(0, -1)}

      const response = await fetch(`${config.urls.READINGS_URL}${qParam}`);
      const data = await response.json();
      console.log(data)
      
      setRawData(data)
    }

    const getDates = (data) => {
      const dates = data[0]["data"].map(
        (reading) => reading["reading_datetime"]
      );
      return dates
    }

    const getAqiData = (data) => {
      const aqiData = data.map((station) => (
        {
          "station_id": station["station_id"],
          "data": station["data"].map((reading) => (reading["pm_25_aqi"]))
      }
      )) 
      return aqiData
    }

    getReadings()
    const newDates = getDates(rawData)
    const newAqiData = getAqiData(rawData)
    console.log('newAqiData')
    console.log(newAqiData)
    setDates(newDates);
    setAqiData(newAqiData)
  }, [idsToGraph]);

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
            handleTempCheckChange={handleTempCheckChange}
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
              onChange={handleStationCheckChange}
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
          {Object.entries(timePeriods).map((item) => (
            <SideDropDownRadio
              key={item[0]}
              name={item[0]}
              checked={item[1]}
              onChange={pickTimePeriod}
            />
          ))}
        </SideDropDown>
        <HomeButton onClick={updateIds} value={"update graph"} />
      </HomeSideBarLeft>

      <HomeGraph />

      <HomeSideBarRight />
    </div>
  );
};

export default Home;
