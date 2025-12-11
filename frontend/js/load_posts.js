$(document).ready(function() {

    const categories = ["Europe", "Asia", "Africa", "North America", "South America", "Australia", "Antarctica"];
    const subcategories = {
        "Europe": ["Austria", "Italy", "United Kingdom"],
        "Asia": ["China", "India"],
        "Africa": ["South Africa"],
        "North America": ["United States", "Canada", "Mexico"],
        "South America": ["Brazil"],
        "Australia": ["Australia"],
        "Antarctica": []
    };
    const filters = ["City", "Nature"];

    let selectedCategories = [];
    let selectedFilters = [];

    function showCategories() {
    let categoryItems = categories.map(category => `
        <li class="nav-item">
            <a class="nav-link category" href="#" data-category="${category}">${category}</a>
        </li>
    `).join("");
    $("#categoryItems").html(categoryItems);
    $("#categoryNavbar").removeClass("d-none");
    }

    function showSubcategories(category) {
        let subcategoryItems = subcategories[category].map(subcategory => `
            <li class="nav-item">
                <a class="nav-link subcategory" href="#" data-subcategory="${subcategory}">${subcategory}</a>
            </li>
        `).join("");
        $("#categoryItems").html(subcategoryItems);
    }

    function showFilters() {
        if ($("#filterItems").children().length === 0) {
        let filterItems = filters.map(filter => `
            <li class="nav-item">
                <a class="nav-link filter" href="#" data-filter="${filter}">${filter}</a>
            </li>
        `).join("");
        $("#filterItems").html(filterItems);
        }
        $("#filterNavbar").removeClass("d-none");
    }

    showCategories();

    $(document).on("click", ".category", function (event) {
        event.preventDefault();
        const category = $(this).data("category");

        if ($(this).hasClass("bg-primary text-white")) {
        $(this).removeClass("bg-primary text-white");
        $("#backToCategories").addClass("d-none");
        return;
        }

        $(".category").removeClass("bg-primary text-white");
        $(this).addClass("bg-primary text-white");

        showSubcategories(category);

        $("#backToCategories").removeClass("d-none");
    });

    $(document).on("click", ".subcategory", function (event) {
        event.preventDefault();
        const subcategory = $(this).data("subcategory");
        $(this).toggleClass("bg-primary text-white");
        if ($(this).hasClass("bg-primary")) {
        selectedCategories.push(subcategory);
        } else {
        selectedCategories = selectedCategories.filter(item => item !== subcategory);
        }
    });

    $(document).on("click", "#backToCategories", function () {
        showCategories();
        $("#backToCategories").addClass("d-none");
    });

    $(document).on("click", ".filter", function (event) {
        event.preventDefault();
        const filter = $(this).data("filter");
        $(this).toggleClass("bg-secondary text-white");
        if ($(this).hasClass("bg-secondary")) {
        selectedFilters.push(filter);
        } else {
        selectedFilters = selectedFilters.filter(item => item !== filter);
        }
    });

    $(document).on("click", "#showFilters", function (event) {
        event.preventDefault();
        if ($("#filterNavbar").hasClass("d-none")) {
        showFilters();
        } else {
        $("#filterNavbar").addClass("d-none");
        }
    });

    function fetchPosts() {
        const path = window.location.pathname; // current path

        if (path === '/posts') {
            fetch('/api/posts')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch posts');
                    }
                    return response.json();
                })
                .then(posts => {
                    const postsListElement = document.getElementById('posts-list');
                    postsListElement.innerHTML = '';

                    posts.forEach(post => {
                        const postElement = document.createElement('div');
                        postElement.classList.add('post');

                        const userElement = document.createElement('div');
                        userElement.classList.add('user');
                        userElement.textContent = `User: ${post.user}`;

                        const textElement = document.createElement('div');
                        textElement.classList.add('text');
                        textElement.textContent = post.text || 'No text';

                        const imageElement = document.createElement('img');
                        imageElement.src = post.image_full;
                        imageElement.alt = post.text || 'Post image';

                        postElement.appendChild(userElement);
                        postElement.appendChild(imageElement);
                        postElement.appendChild(textElement);

                        postsListElement.appendChild(postElement);
                    });
                })
                .catch(error => {
                    console.error('Error fetching posts:', error);
                    const postsListElement = document.getElementById('posts-list');
                    postsListElement.innerHTML = '<p>No posts yet</p>';
                });
        } else if (path.startsWith('/users/')) {
            const username = path.split('/')[2]; // get username from path

            fetch(`/api/users/${username}/posts`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch posts for user');
                    }
                    return response.json();
                })
                .then(posts => {
                    const postsListElement = document.getElementById('posts-list');
                    postsListElement.innerHTML = '';

                    posts.forEach(post => {
                        const postElement = document.createElement('div');
                        postElement.classList.add('post');

                        const userElement = document.createElement('div');
                        userElement.classList.add('user');
                        userElement.textContent = `User: ${post.user}`;

                        const textElement = document.createElement('div');
                        textElement.classList.add('text');
                        textElement.textContent = post.text || 'No text';

                        const imageElement = document.createElement('img');
                        imageElement.src = post.image;
                        imageElement.alt = post.text || 'Post image';

                        postElement.appendChild(userElement);
                        postElement.appendChild(imageElement);
                        postElement.appendChild(textElement);

                        postsListElement.appendChild(postElement);
                    });
                })
                .catch(error => {
                    console.error('Error fetching posts:', error);
                    const postsListElement = document.getElementById('posts-list');
                    postsListElement.innerHTML = '<p>No posts yet</p>';
                });
        }
    }

    fetchPosts();
});
