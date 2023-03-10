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
    "12 hr": true,
    "24 hr": false,
    "48 hr": false,
    "5 day": false,
    "10 day": false,
    "1 month": false,
    "1 year": false,
    "all time": false,
  });
  const [stations, setStations] = useState([{station_id: "840360470118", station_name: "Bklyn - PS274", checked: true}]);
  const [tempStations, setTempStations] = useState(null);
  const [tempTempStations, setTempTempStation] = useState(null);
  const [leftSideBarVisible, setLeftSideBarVisible] = useState(true);
  const [stationDropVisible, setStationDropVisible] = useState(true);
  const [editStationPopupVisible, setEditStationPopupVisible] = useState(false);
  const [timeDropVisible, setTimeDropVisible] = useState(true);
  const [zipcode, setZipcode] = useState("11206");
  const [zipQuery, setZipQuery] = useState("11206");
  const [rawReadings, setRawReadings] = useState({});
  const [dates, setDates] = useState([]);
  const [aqiData, setAqiData] = useState([]);
  const [idsToGraph, setIdsToGraph] = useState(["840360470118"]);

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
    const trueStations = tempStations.map((stn) =>
      stn["checked"] === true
        ? {
            station_id: stn["station_id"],
            station_name: stn["station_name"],
            checked: true,
            latitude: stn["latitude"],
            longitude: stn["longitude"],
            location_coord: stn["location_coord"],
          }
        : null
    );
    const newStations = trueStations.filter(Boolean);
    setStations(newStations);
    toggleEditStationPopup();
  };

  const updateIds = () => {
    const newIds = [];
    stations.forEach((stn) => {
      if (stn["checked"]) {
        newIds.push(stn["station_id"]);
      }
    });
    setIdsToGraph(newIds);
  };

  const handleStationCheckChange = (e) => {
    const updatedStations = [...stations];
    updatedStations.forEach((stn) => {
      if (stn["station_id"] === e.target.name) {
        stn["checked"] = !stn["checked"];
      }
    });
    setStations(updatedStations);
  };

  const handleTempCheckChange = (e) => {
    const updatedTempStations = [...tempStations];
    updatedTempStations.forEach((stn) => {
      if (stn["station_id"] === e.target.name) {
        stn["checked"] = !stn["checked"];
      }
    });
    setTempStations(updatedTempStations);
  };

  const getReadings = async (ids, period) => {
    let qParam = ids.reduce((prev, id) => prev + `ids=${id}&`, "?");
    if (qParam.slice(-1) === "&") {
      qParam = qParam.slice(0, -1);
    }
    const response = await fetch(`${config.urls.READINGS_URL}${qParam}`);
    const data = await response.json();

    return data;
  };

  const getStationName = (stationID) => {
    const stn = stations.filter((s) => (s["station_id"] === stationID))
    const stnName = stn["station_name"]
    return stnName
  }

  /**
   * takes object station_ids and requested pollutants for each station
   * returns aqiData obj to be passed to HomeGraph
   */
  const transformAQIData = (stationPollutantObj) => {
  }

  
  /**
   * func (and hook below) for grabbing aqi data for selected stations
   */
  const handleReadingDataChange = async () => {
    const data = await getReadings(idsToGraph);
    console.log(data)
    const dates = data[0]["readings"].map(
      (reading) => reading["reading_datetime"]
    );
    const aqiData = data.map((stn) => ({
      station_id: stn["station_id"],
      data: stn["readings"].map((reading) => reading["pm25_aqi"]),
    }));

    setRawReadings(data);
    setDates(dates);
    setAqiData(aqiData);
  };

  useEffect(() => {
    if (idsToGraph.length > 0) {
      handleReadingDataChange();
    }
  }, [idsToGraph]);

  /**
   * hook for getting the pollutants that each station has available to plot
   * sorry for the mess
   */
  useEffect(() => {
    const getTempStationPollutants = async () => {
      if (!tempTempStations) return;
      else {
        const ids = tempTempStations.map((stn) => stn["station_id"]);
        const data = await getReadings(ids);
        const newTemps = tempTempStations.map((stn) => {
          const dReadings = data.filter((dstn) => {
            return dstn["station_id"] === stn["station_id"];
          });
          const dpollutants = dReadings[0]["readings"][0]
            ? Object.entries(dReadings[0]["readings"][0]).filter(
                ([key, value]) => key.slice(-3) === "aqi" && value
              ).map(([key, value]) => key)
            : null;
          stn["pollutants"] = dpollutants;
          return stn;
        });
        setTempStations(newTemps);
      }
    };
    getTempStationPollutants();
  }, [tempTempStations]);

  /**
   * hook for finding stations near zipcode, runs on button click from editStationWindow
   */
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
      tempArrTwo.forEach((stn) => (stn["checked"] = false));

      setTempTempStation(tempArrTwo);
    };
    findStations();
  }, [zipQuery]);

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

      <HomeGraph dates={dates} aqiData={aqiData} />

      <HomeSideBarRight />
    </div>
  );
};

export default Home;
