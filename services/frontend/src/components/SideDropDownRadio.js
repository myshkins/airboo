const SideDropDownRadio = (props) => {
  return (
    <div className="dropdown-input-wrap">
      <label>
        <input
          type="radio"
          name={props.name}
          onChange={props.onChange}
          checked={props.checked}
        />
        {props.name}
      </label>
    </div>
  );
};

export default SideDropDownRadio;
