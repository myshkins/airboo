const SideDropDownRadio = (props) => {
  return (
    <div className="dropdown-input-wrap">
      <input
        type="radio"
        name={props.name}
        onChange={props.onChange}/>
      <label htmlFor={props.name}>{props.value}</label>
    </div>
  )
}

export default SideDropDownRadio