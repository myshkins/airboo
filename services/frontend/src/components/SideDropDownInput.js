const SideDropDownInput = (props) => {
  return (
    <div className="dropdown-input-wrap">
      <input type={props.type} name={props.name} />
      <label htmlFor={props.name}>{props.value}</label>
    </div>
  )
}

export default SideDropDownInput