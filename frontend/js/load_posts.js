$(document).ready(function() {

    const categories = ["Europe", "Asia", "Africa", "North America", "South America", "Australia"];
    const subcategories = {
        "Europe": ["Austria", "Italy", "United Kingdom"],
        "Asia": ["China", "India"],
        "Africa": ["South Africa"],
        "North America": ["United States", "Canada", "Mexico"],
        "South America": ["Brazil"],
        "Australia": ["Australia"]
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
        $(".category").removeClass("bg-primary text-white");
        $(this).addClass("bg-primary text-white");
        showSubcategories(category);
        $("#backToCategories").removeClass("d-none");

        updateURL();
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

        updateURL();
    });

    $(document).on("click", "#backToCategories", function () {
        selectedCategories = [];
        updateURL();
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

        updateURL();
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
        const params = new URLSearchParams(window.location.search);
        const countryParam = params.get("country");
        const filterParam = params.get("filter");
        const username = window.location.pathname.split('/')[2];

        let apiUrl = '/api/posts';
        if (window.location.pathname.startsWith('/users/') && username) {
            apiUrl = `/api/users/${username}/posts`;
        }

        const urlParams = [];
        if (countryParam) urlParams.push(`country=${countryParam}`);
        if (filterParam) urlParams.push(`filter=${filterParam}`);
        if (urlParams.length > 0) {
            apiUrl += `?${urlParams.join('&')}`;
        }

        fetch(apiUrl)
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

    fetchPosts();

    function updateURL() {
    const params = new URLSearchParams();

    if (selectedCategories.length > 0) {
        params.set("country", selectedCategories.join(","));
    }
    if (selectedFilters.length > 0) {
        params.set("filter", selectedFilters.join(","));
    }

    let newUrl = '/posts';
    const pathParts = window.location.pathname.split('/').filter(Boolean);
    
    if (pathParts[0] === 'users' && pathParts[1]) {
        newUrl = `/users/${pathParts[1]}/posts`;
    }
    if (params.toString()) {
        newUrl += `?${params.toString()}`;
    }

    window.history.pushState({}, "", newUrl);
    fetchPosts();
    }

});
