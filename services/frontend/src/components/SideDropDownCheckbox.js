const SideDropDownCheckbox = (props) => {
  return (
    <div className="dropdown-input-wrap">
      <label>
        <input
        type="checkbox"
        name={props.name}
        checked={props.checked}
        onChange={props.onChange}/>
        <span>{props.value}</span>
      </label>
    </div>
  )
}

export default SideDropDownCheckbox