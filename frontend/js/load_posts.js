$(document).ready(function() {
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
