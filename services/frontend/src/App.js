import './App.css';
import Nav from './components/Nav';
import Home from './pages/Home';
import About from './pages/About';
import Contact from './pages/Contact';
import Profile from './pages/Profile';
import { Route, Routes } from 'react-router-dom';
import React, { useEffect, useState } from 'react';

function App() {
  const [stations, setStations] = useState([])
  const [leftSideBarVisible, setLeftSideBarVisible] = useState(true)
  const [stationDropVisible, setStationDropVisible] = useState(true)
  const [timeDropVisible, setTimeDropVisible] = useState(true)

  const toggleSideBar = () => {
    setLeftSideBarVisible(!leftSideBarVisible)
  }

  const toggleStationDrop = () => {
    setStationDropVisible(!stationDropVisible)
  }

  const toggleTimeDrop = () => {
    setTimeDropVisible(!timeDropVisible)
  }

  useEffect(() => {
    let ignore = false

    // change this to an async func that grabs real station data
    const fetchStations = () => {
      const stations = ["Brooklyn, NY", "Queens, NY", "Jersey City, NJ"]
      if (!ignore) setStations(stations)
    }

    fetchStations()
    return () => { ignore = true }
  }, [Home])

  return (
    <div>
      <Nav />
      <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'></link>
      <div className='container'>
        <Routes>
          <Route path='/'
            element={
              <Home 
                stations={stations}
                leftSideBarVisible={leftSideBarVisible}
                toggleSideBar={toggleSideBar}
                stationDropVisible={stationDropVisible}
                toggleStationDrop={toggleStationDrop}
                timeDropVisible={timeDropVisible}
                toggleTimeDrop={toggleTimeDrop}/>
            } />
          <Route path='/about' element={<About />} />
          <Route path='/contact' element={<Contact />} />
          <Route path='/profile' element={<Profile />} />
        </Routes>
      </div>
    </div>

  );
}

export default App;
