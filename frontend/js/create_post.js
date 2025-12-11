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
    });


    $(document).on("click", ".subcategory", function (event) {
        event.preventDefault();
        const subcategory = $(this).data("subcategory");
        if ($(this).hasClass("bg-primary text-white")) {
            $(this).removeClass("bg-primary text-white");
            selectedCategories = selectedCategories.filter(item => item !== subcategory);
        } else {
            $(".subcategory").removeClass("bg-primary text-white");
            selectedCategories = [subcategory];
            $(this).addClass("bg-primary text-white");
        }

    });

    $(document).on("click", "#backToCategories", function () {
        selectedCategories = [];
        showCategories();

        $("#backToCategories").addClass("d-none");
    });


    $(document).on("click", ".filter", function (event) {
        event.preventDefault();
        const filter = $(this).data("filter");
        if ($(this).hasClass("bg-secondary text-white")) {
            $(this).removeClass("bg-secondary text-white");
            selectedFilters = selectedFilters.filter(item => item !== filter);
        } else {
            $(".filter").removeClass("bg-secondary text-white");
            selectedFilters = [filter];
            $(this).addClass("bg-secondary text-white");
        }
    });

    if ($("#filterNavbar").hasClass("d-none")) {
        showFilters();
        } else {
        $("#filterNavbar").addClass("d-none");
    }

    $("#create-post-form").on("submit", function(event) {
        event.preventDefault();
        const loggedInUser = localStorage.getItem("loggedInUser");

        const postData = {
            user: loggedInUser,
            image: $("#image").val(),
            text: $("#content").val(),
            country: selectedCategories[0] || "",
            filter: selectedFilters[0] || "",
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