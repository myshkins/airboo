import HomeButton from "./HomeButton";
import SideDropDownInput from "./SideDropDownCheckbox";

const EditStationsWindow = (props) => {
  return (
    <div className="edit-station-window">
      <h3>Add/Remove Stations</h3>
      <div>
        <label htmlFor="zipcode-input">zipcode</label>
        <input
          type="text"
          name="zipcode-input"
          value={props.zipcode}
          onChange={props.handleZipcodeChange}
        />
        <HomeButton
          value={"find stations"}
          onClick={props.handleZipQueryChange}
        />
      </div>
      {props.tempStations != null ? <h5>select stations to include</h5> : null}
      <div>
        <form onSubmit={props.updateStations}>
          {props.tempStations.map((station) => (
            <SideDropDownInput
              key={station["station_id"]}
              name={station["station_id"]}
              value={station["station_name"]}
              checked={station["checked"]}
              onChange={props.handleTempCheckChange}
              type="checkbox"
            />
          ))}
          <input type="submit" value="update stations" />
        </form>
      </div>
    </div>
  );
};

export default EditStationsWindow;
