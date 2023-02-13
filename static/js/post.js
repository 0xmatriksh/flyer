// COMMENT: THIS IS BIZZARE CODE
// ALSO IN HTML PART OF REPLIES
// need to implement technique to auto create the ui in depth layer for reply of replys without manuall html elements
// cause depth can do to too deep, so need to handle that

document.querySelector("#replybtn").addEventListener("click", function () {
    console.log("reply clicked")
    const formElem = document.createElement("form");
    formElem.setAttribute("method", "post")
    formElem.setAttribute("action", `/reply/${this.dataset.post}/${this.dataset.cmnt}`)
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

document.querySelector("#replybtn1").addEventListener("click", function () {
    console.log("reply clicked")
    const formElem = document.createElement("form");
    formElem.setAttribute("method", "post")
    formElem.setAttribute("action", `/reply/${this.dataset.post}/${this.dataset.cmnt}`)
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
    this.after(formElem)
    this.setAttribute("disabled", "true")
})

document.querySelector("#replybtn2").addEventListener("click", function () {
    console.log("reply clicked")
    const formElem = document.createElement("form");
    formElem.setAttribute("method", "post")
    formElem.setAttribute("action", `/reply/${this.dataset.post}/${this.dataset.cmnt}`)
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
    this.after(formElem)
    this.setAttribute("disabled", "true")
})

// document.getElementById("reply").addEventListener("click", function () {
//     console.log("sent request")
// })