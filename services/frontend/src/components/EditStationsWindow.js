import HomeButton from "./HomeButton";

const EditStationsWindow = (props) => {
  return (
    <div className="edit-station-window">
      <h3>Add/Remove Stations</h3>
      <form onSubmit={props.findStations}>
        <label htmlFor="zipcode-input">zipcode</label>
        <input type="text" name="zipcode-input"></input>
        <input type="submit" value="find stations" />
        <HomeButton value="update stations" onClick={props.updateStations} />
      </form>
    </div>
  );
};

export default EditStationsWindow;
