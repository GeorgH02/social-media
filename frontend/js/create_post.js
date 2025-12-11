$(document).ready(function() {
$("#create-post-form").on("submit", function(event) {
    event.preventDefault();
    const loggedInUser = localStorage.getItem("loggedInUser");

    const postData = {
        user: loggedInUser,
        image_full: $("#image").val(),
        text: $("#content").val(),
    };

    fetch('/api/posts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            alert("Post created successfully!");
            $("#create-post-form")[0].reset();
        } else {
            alert("Error creating post");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error while creating post");
    });
});
});