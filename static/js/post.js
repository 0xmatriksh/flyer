// COMMENT: THIS IS BIZZARE CODE
// ALSO IN HTML PART OF REPLIES
// need to implement technique to auto create the ui in depth layer for reply of replys without manuall html elements
// cause depth can do to too deep, so need to handle that

var replyForm = '';
function showReplyFrom(element) {
    const allforms = document.querySelectorAll('.replyForm');
    allforms.forEach(function (form) {
        form.style.display = "none";
    })

    element.nextElementSibling.style.display = "block"

    const allform = document.querySelectorAll('.replyForm');
    allform.forEach(function (form) {
        if (form.style.display == "block") {
            replyForm = form;
        }
    })
}

// CODE TO NOT COMMENT IF the commment box is EMPTY

// function sleep(time) {
//     return new Promise((resolve) => setTimeout(resolve, time));
// }

// window.onload = function () {
//     const allform = document.querySelectorAll('.replyForm');
//     allform.forEach(function (form) {
//         if (form.style.display == "block") {
//             replyForm = form;
//         }
//     })
// }


function submitReplyForm(element) {
    // event.preventDefault();

    const formData = new FormData(replyForm);

    const postId = document.getElementById("postId").innerText;
    const commentId = document.getElementById("commentId").innerText;

    const replyText = document.getElementById("replyText").value;
    console.log(replyText)

    if (replyText == "") {
        alert("Cannot comment Empty");
    }
    else {
        console.log(formData);
        // Send the form data to Flask web app using fetch
        fetch(`/reply/${postId}/${commentId}`, {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
            })
            .catch(error => {
                console.error('Error:', error);
            });
        location.reload()
    }
}

// CODE TO NOT COMMENT IF the commment box is EMPTY
const myForm = document.querySelector("#commentForm")

myForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const postId = document.getElementById("postId").innerText
    const formData = new FormData(myForm);

    const commentText = document.getElementById("commentText").value;
    if (commentText == "") {
        alert("Cannot comment Empty");
        console.log(postId)
    }
    else {
        console.log(formData)
        // Send the form data to Flask web app using fetch
        fetch(`/comment/${postId}`, {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
            })
            .catch(error => {
                console.error('Error:', error);
            });
        location.reload()
    }
})

