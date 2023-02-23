const SideDropDownCheckbox = (props) => {
  return (
    <div className="dropdown-input-wrap" onClick={props.onChange}>
      <input
        type="checkbox"
        name={props.name}
        checked={props.checked}
        onChange={props.onChange}/>
      <label htmlFor={props.name}>{props.value}</label>
      <ul>
        {props.pollutants.map((pollutant) => (
          <li></li>
        ))}
      </ul>
    </div>
  )
}

export default SideDropDownCheckbox
