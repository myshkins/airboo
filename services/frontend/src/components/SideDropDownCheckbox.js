const SideDropDownCheckbox = (props) => {
  return (
    <div className="dropdown-input-wrap">
      <input
        type="checkbox"
        name={props.name}
        checked={props.checked}
        onChange={props.onChange}/>
      <label htmlFor={props.name}>{props.value}</label>
    </div>
  )
}

export default SideDropDownCheckbox