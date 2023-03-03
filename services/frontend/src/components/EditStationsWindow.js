import HomeButton from "./HomeButton";
import AddStationCheckbox from "./AddStationCheckbox";

const EditStationsWindow = (props) => {
  return (
    <div className="edit-station-window">
      <h3>Add/Remove Stations</h3>
      <div className={"add-remove-wrap"}>
        <div className="add-remove-zip-entry">
          <label htmlFor="zipcode-input">zipcode:</label>
          <input
            type="text"
            name="zipcode-input"
            value={props.zipcode}
            onChange={props.handleZipcodeChange}
          />
        </div>
        <HomeButton
          value={"find stations"}
          onClick={props.handleZipQueryChange}
        />
      </div>
      {props.tempStations != null ? <h5>select stations to include</h5> : null}
      <div>
        <form onSubmit={props.updateStations}>
          {props.tempStations.map((station) => (
            <AddStationCheckbox
              key={station["station_id"]}
              name={station["station_id"]}
              pollutants={station["pollutants"]}
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
