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
      <ul>
        {props.pollutants ? (
          <ul>
            {props.pollutants.map((pollutant) => (
              <li key={pollutant}>{pollutant}</li>
            ))}
          </ul>
        ) : null}
      </ul>
    </div>
  );
};

export default AddStationCheckbox;
