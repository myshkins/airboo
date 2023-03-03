const AddStationCheckbox = (props) => {
  return (
    <div className="dropdown-input-wrap">
      <label>
        <input
          type="checkbox"
          name={props.name}
          checked={props.checked}
          onChange={props.onChange}
        />
        <span>{props.value}</span>
      </label>
      {props.pollutants ? (
        <ul className={"add-station-pollutant"}>
          {props.pollutants.map((pollutant) => (
            <li key={pollutant} className={"add-station-pollutant"}>{pollutant.slice(0, -4)}</li>
          ))}
        </ul>
      ) : null}
    </div>
  );
};

export default AddStationCheckbox;
