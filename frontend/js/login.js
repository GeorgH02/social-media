$(document).ready(function() {
    $("#login-form").on("submit", function(event) {
        event.preventDefault();

        const userData = {
            user: $("#username").val(),
        };

        fetch(`/api/users/${userData.user}`)
            .then(response => {
                if (response.ok) {
                    // if user exists log in
                    localStorage.setItem("loggedInUser", userData.user);
                    alert("Logged in successfully!");
                    window.location.href = "posts";
                    $("#login-form")[0].reset();



                } else if (response.status === 404) {
                    // if user does not exist make new user
                    fetch('/api/users', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ name: userData.user }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.id) {
                            localStorage.setItem("loggedInUser", userData.user);
                            alert("User created and logged in successfully!");
                            window.location.href = "posts";
                            $("#login-form")[0].reset();
                        } else {
                            alert("Error creating user");
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert("Error while creating user");
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Error while logging in");
            });
    });
});
