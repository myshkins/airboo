import SideDropDownInput from "./SideDropDownInput";

const EditStationsWindow = (props) => {
  return (
    <div className="edit-station-window">
      <h3>Add/Remove Stations</h3>
      <form onSubmit={props.findStations}>
        <label htmlFor="zipcode-input">zipcode</label>
        <input type="text" name="zipcode-input"></input>
        <input type="submit" value="find stations" />
      </form>
      {props.tempStations != null ? (
        <div>
          <h5>select stations to include</h5>
          <form onSubmit={props.updateStations}>
          {props.tempStations.map((station) => (
            <SideDropDownInput
              key={station["location_coord"]}
              name={station["station_id"]}
              value={station["station_name"]}
              onChange={props.handleCheckChange}
              type="checkbox" />
          ))}            
          <input type="submit" value="update stations"/>
          </form>
        </div>
      ) : null}
    </div>
  );
};

export default EditStationsWindow;
