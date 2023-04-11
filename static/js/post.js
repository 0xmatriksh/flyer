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


    const postId = element.querySelector("#postId").innerText;
    const commentId = element.querySelector("#commentId").innerText;

    const replyText = element.querySelector("#replyText").value;

    if (replyText == "") {
        alert("Cannot reply Empty");
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
        // console.log(formData)
        // Send the form data to Flask web app using fetch
        fetch(`/comment/${postId}`, {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                location.reload();
            })
            .catch(error => {
            });

        function myfunc() {
            // redirect after commenting
            console.log('111')
            location.href = `http://127.0.0.1:5000/post/${postId}`;
        }

        setTimeout(myfunc, 1000)
    }

})

