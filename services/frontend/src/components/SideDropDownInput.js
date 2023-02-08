const SideDropDownInput = (props) => {
  return (
    <div className="dropdown-input-wrap">
      <input type={props.type} name={props.name} onChange={props.onChange}/>
      <label htmlFor={props.name}>{props.value}</label>
    </div>
  )
}

export default SideDropDownInput