

$(document).ready(function() {
    function fetchUsers() {
        fetch('/api/users')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch users');
                }
                return response.json();
            })
            .then(users => {
                const usersListElement = document.getElementById('users-list');
                usersListElement.innerHTML = '';

                users.forEach(user => {
                    const userCard = document.createElement('div');
                    userCard.classList.add('user-card');

                    const usernameElement = document.createElement('div');
                    usernameElement.classList.add('username');
                    usernameElement.textContent = user.name;

                    const viewButton = document.createElement('button');
                    viewButton.classList.add('btn', 'btn-primary');
                    viewButton.textContent = 'View Posts';
                    viewButton.onclick = function() {
                        window.location.href = `/users/${user.name}/posts`;
                    };

                    userCard.appendChild(usernameElement);
                    userCard.appendChild(viewButton);

                    usersListElement.appendChild(userCard);
                });
            })
            .catch(error => {
                console.error('Error fetching users:', error);
                const usersListElement = document.getElementById('users-list');
                usersListElement.innerHTML = '<p>No users yet</p>';
            });
    }

    fetchUsers();
});
