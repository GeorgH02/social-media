$(document).ready(function () {
  updateNavbar();

  function updateNavbar() {
    const loggedInUser = localStorage.getItem("loggedInUser");
    let leftContent = `
            <li class="nav-item">
                <a class="nav-link" href="/posts">Home</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/users">Users</a>
            </li>
        `;

    

    let rightContent = "";
    if (loggedInUser) {
        rightContent += `
            <li class="nav-item dropdown profile">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Hello, ${loggedInUser}
                </a>
                <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <li><a class="dropdown-item" href="">My Profile</a></li>
                    <li><a class="dropdown-item" href="">My Content</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="" id="sign-out">Logout</a></li>
                </ul>
            </li>
        `;

        leftContent += `
            <li class="nav-item">
                <a class="nav-link" href="/create_post">Create a new Post</a>
            </li>
        `;

    } else {
        rightContent += `
            <li class="nav-item">
            <a class="nav-link" href="/login">Login</a>
            </li>
        `; 
    }
    
    $("#navbarNav .me-auto").html(leftContent);
    $("#right-nav-items").html(rightContent);
  }

  $(document).on("click", "#sign-out", function (event) {

    event.preventDefault();
    localStorage.removeItem("loggedInUser");
    updateNavbar();
    window.location.href = "/posts";
  });

});
