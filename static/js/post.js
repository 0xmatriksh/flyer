document.getElementById("replybtn").addEventListener("click", function () {
    console.log("reply clicked")
    const formElem = document.createElement("form");
    formElem.setAttribute("method", "post")
    formElem.setAttribute("action", `/reply/${this.dataset.post}`)
    const txtElem = document.createElement("textarea")
    txtElem.setAttribute("name", "cmnt")
    txtElem.setAttribute("rows", "6")
    txtElem.setAttribute("cols", "60")
    formElem.appendChild(txtElem)
    const btnElem = document.createElement("button")
    btnElem.setAttribute("id", "reply")
    btnElem.setAttribute("type", "submit")
    // btnElem.setAttribute("data-postid", this.dataset.post)
    btnElem.innerText = "submit"
    formElem.appendChild(btnElem)
    document.getElementById("replybtn").after(formElem)
    document.getElementById("replybtn").setAttribute("disabled", "true")
})

// document.getElementById("reply").addEventListener("click", function () {
//     console.log("sent request")
// })