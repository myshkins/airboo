import Foco from "react-foco";
import React, { useEffect, useState } from "react";

import { config } from "../Constants";
import EditStationsWindow from "../components/EditStationsWindow";
import getReadings from "../components/hooks/GetReadings";
import HomeButton from "../components/HomeButton";
import HomeGraph from "../components/HomeGraph";
import HomeSideBarLeft from "../components/HomeSideBarLeft";
// import HomeSideBarRight from "../components/HomeSideBarRight";
import SideDropDown from "../components/SideDropDown";
import SideDropDownCheckbox from "../components/SideDropDownCheckbox";
import SideDropDownRadio from "../components/SideDropDownRadio";
import TimePeriod from "../components/util/timePeriodEnum";

import "./Home.css";

const Home = () => {
  const [aqiData, setAqiData] = useState([]);
  const [dates, setDates] = useState([]);
  const [editStationPopupVisible, setEditStationPopupVisible] = useState(false);
  const [idsToGraph, setIdsToGraph] = useState(["840360470118"]);
  const [leftSideBarVisible, setLeftSideBarVisible] = useState(true);
  const [pollutants, setPollutants] = useState({
    pm25: false,
    pm10: false,
    o3: false,
    co: false,
    no2: false,
    so2: false,
  });
  const [pollutantDropVisible, setPollutantDropVisible] = useState(true);
  const [tempStations, setTempStations] = useState(null);
  const [tempTempStations, setTempTempStations] = useState(null);
  const [timeDropVisible, setTimeDropVisible] = useState(true);
  const [timePeriod, setTimePeriod] = useState(new TimePeriod("12hr"));
  const [stations, setStations] = useState([
    {
      station_id: "840360470118",
      station_name: "Bklyn - PS274",
      checked: true,
    },
  ]);
  const [stationDropVisible, setStationDropVisible] = useState(true);
  const [zipcode, setZipcode] = useState("11206");
  const [zipQuery, setZipQuery] = useState("11206");

  const toggleSideBar = () => {
    setLeftSideBarVisible(!leftSideBarVisible);
  };

  const toggleStationDrop = () => {
    setStationDropVisible(!stationDropVisible);
  };

  const toggleTimeDrop = () => {
    setTimeDropVisible(!timeDropVisible);
  };

  const togglePollutantDrop = () => {
    setPollutantDropVisible(!pollutantDropVisible);
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
    setTimePeriod(new TimePeriod(e.target.name));
  };

  const handlePollutantChange = (e) => {
    const newPollutants = { ...pollutants };
    newPollutants[e.target.name] = !newPollutants[e.target.name];
    setPollutants(newPollutants);
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

  const makeQuery = (ids, period = 0, pollutants = "") => {
    let qParams = ids
      .reduce((prev, id) => prev + `ids=${id}&`, "?")
      .slice(0, -1);
    let timeParam = "";
    if (period !== 0) {
      timeParam = `&period=${period.query()}`;
    }
    let truePollutants = [];
    if (pollutants !== "") {
      truePollutants = Object.entries(pollutants).reduce(
        (prev, [key, value]) => {
          if (value) {
            prev.push(key);
          }
          return prev;
        },
        []
      );
    }
    const pollutantsParam =
      truePollutants.length === 0
        ? ""
        : `&pollutants=${truePollutants.join("&pollutants=")}`;
    qParams = qParams + timeParam + pollutantsParam;
    return qParams;
  };

  const getReadings = async (ids, period, pollutants) => {
    const params = makeQuery(ids, period, pollutants);
    const response = await fetch(`${config.urls.READINGS_URL}${params}`);
    const data = await response.json();
    return data;
  };

  const getStationName = (stationID) => {
    const stn = stations.filter((s) => s["station_id"] === stationID)[0];
    const stnName = stn["station_name"];
    return stnName;
  };

  const getDates = (data) => {
    const dates = data[0]["readings"].map(
      (reading) => reading["reading_datetime"]
    );
    return dates;
  };

  /**
   * Hook for grabbing aqi data for selected stations
   */

  useEffect(() => {
    if (idsToGraph.length > 0) {
      const handleReadingDataChange = async () => {
        const data = await getReadings(idsToGraph, timePeriod, pollutants);
        const dates = getDates(data);
        const aqiData = data.map((pollut) => ({
          datasetName:
            getStationName(pollut["station_id"]) + " : " + pollut["pollutant"],
          data: pollut["readings"].map(
            (reading) => reading[`${pollut["pollutant"]}_aqi`]
          ),
        }));

        setDates(dates);
        setAqiData(aqiData);
      };
      handleReadingDataChange();
    }
  }, [idsToGraph]);

  /**
   * Hook for finding stations near zipcode, runs on button click from
   * editStationWindow. getTempStationPollutants will run after this hook
   * updates tempTempStations.
   */
  useEffect(() => {
    const getTempStationPollutants = async () => {
      if (!tempTempStations) return;
      const ids = tempTempStations.map((stn) => stn["station_id"]);
      const params = makeQuery(ids);
      const response = await fetch(`${config.urls.POLLUTANTS_URL}${params}`);
      const tempPollutants = await response.json();
      let ttStations = [...tempTempStations];
      ttStations.forEach((stn) => {
        stn["checked"] = false;
        try {
          const stnPollutants = tempPollutants["pollutants"].find(
            (s) => s["station_id"] === stn["station_id"]
          );
          stn["pollutants"] = stnPollutants["pollutants"];
        } catch (e) {
          if (e instanceof TypeError) {
            stn["pollutants"] = [];
          } else {
            throw e;
          }
        }
      });
      setTempStations(ttStations);
    };
    getTempStationPollutants();
  }, [tempTempStations]);

  useEffect(() => {
    const findStations = async () => {
      const response = await fetch(`${config.urls.STATIONS_URL}${zipcode}`);
      const data = await response.json();
      const tempArr = [...data, ...stations];
      const tempArrTwo = tempArr.filter(
        (value, index, arr) =>
          index ===
          arr.findIndex((item) => item["station_id"] === value["station_id"])
      );
      setTempTempStations(tempArrTwo);
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
          <Foco onClickOutside={toggleEditStationPopup}>
            <EditStationsWindow
              zipcode={zipcode}
              tempStations={tempStations}
              updateStations={updateStations}
              handleTempCheckChange={handleTempCheckChange}
              handleZipcodeChange={handleZipcodeChange}
              handleZipQueryChange={handleZipQueryChange}
            />
          </Foco>
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
          name={"pollutants"}
          onclick={togglePollutantDrop}
          contentVisible={pollutantDropVisible}
          hasBtn={false}
        >
          {Object.entries(pollutants).map((pollutant) => (
            <SideDropDownCheckbox
              key={pollutant[0]}
              name={pollutant[0]}
              value={pollutant[0]}
              checked={pollutant[1]}
              onChange={handlePollutantChange}
            />
          ))}
        </SideDropDown>
        <SideDropDown
          name={"time period"}
          onClick={toggleTimeDrop}
          contentVisible={timeDropVisible}
          hasBtn={false}
        >
          {Object.entries(timePeriod.table).map((item) => (
            <SideDropDownRadio
              key={item[0]}
              name={item[0]}
              checked={item[0] === timePeriod.key ? true : false}
              onChange={pickTimePeriod}
            />
          ))}
        </SideDropDown>
        <HomeButton onClick={updateIds} value={"update graph"} />
      </HomeSideBarLeft>

      <HomeGraph dates={dates} aqiData={aqiData} />
    </div>
  );
};

export default Home;
