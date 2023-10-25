function Checkbox({index, label, checkHandler, checkedStatus}) {
    return (
        <div className="toggleOption">
            <input 
                type="checkbox"
                id={index}
                name={index}
                value={index}
                checked={checkedStatus}
                onChange={checkHandler}>
            </input>
            <label htmlFor={index}>{label}</label>
        </div>
    )
}

export default Checkbox;