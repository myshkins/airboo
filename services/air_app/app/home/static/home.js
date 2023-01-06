
function toggleDropDown(e) {
    function toggle(d) {d.classList.toggle('hidden')}
    if (e.target.classList.contains("dropdown-btn")) {
        const dropDown = e.target.nextElementSibling
        toggle(dropDown)
    } else if (e.target.classList.contains("bx-chevron-down")) {
        const dropdownBtn = e.target.parentElement
        const dropDown = dropdownBtn.nextElementSibling
        toggle(dropDown)
    }

}


const dropDowns = document.querySelectorAll('.dropdown-btn')
dropDowns.forEach((btn) => {
    btn.addEventListener('click', toggleDropDown)
})