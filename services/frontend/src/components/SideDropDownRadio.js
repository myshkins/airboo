const SideDropDownRadio = (props) => {
  return (
    <div className="dropdown-input-wrap">
      <input
        type="radio"
        name={props.name}
        onChange={props.onChange}
        checked={props.checked}/>
      <label htmlFor={props.name}>{props.name}</label>
    </div>
  )
}

export default SideDropDownRadio