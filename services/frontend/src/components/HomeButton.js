const HomeButton = (props) => {
  return (
    <button onClick={props.onClick} className="btn-home">{props.value}</button>
  )
}

export default HomeButton