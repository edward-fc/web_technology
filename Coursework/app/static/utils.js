// Description: JavaScript file for the AJAX functionality of the application.
// It contains functions to filter dropdowns, select dropdown items, show/hide dropdowns, and execute search.
// The functions are assigned to the global window object to be accessible from other scripts.

// Function to show more comments
function showMoreComments(postId, currentUserId) {
    const commentsContainer = document.getElementById(`comments-${postId}`);
    const currentCommentCount = commentsContainer.childElementCount;
    const moreButton = document.getElementById(`more-button-${postId}`);
    const lessButton = document.getElementById(`less-button-${postId}`);

    // Fetch more comments starting from the current number of displayed comments
    fetch(`/comments/${postId}?limit=${currentCommentCount + 3}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            commentsContainer.innerHTML = '';

            data.comments.forEach(comment => {
                let commentHtml = '';
                let editDeleteButtons = '';

                // Check if the current user is the author of the comment
                if (comment.user_id === currentUserId) {
                    // Add edit and delete buttons for the comment author
                    editDeleteButtons = `
                        <div class="d-flex justify-content-end mt-2">
                            <a href="/edit_post/${comment.id}" class="btn btn-primary mr-2">Edit</a>
                            <form action="/delete_post/${comment.id}" method="POST" style="display: inline;">
                                <button type="submit" class="btn btn-danger" onclick="return confirm('Are you sure you want to delete this comment?')">Delete</button>
                            </form>
                        </div>
                    `;
                }
                // Create the HTML for each comment
                commentHtml += `
                    <div class="border p-3 mb-2">
                        <b>${comment.username}</b>: <strong>${comment.title}</strong><br>
                        <p class="mt-1">${comment.description}</p>
                        ${editDeleteButtons}
                    </div>
                `;
                // add the html to innerHTML
                commentsContainer.innerHTML += commentHtml;
            });

            // Show the Less button if more than 3 comments are displayed
            if (data.comments.length > 3) {
                lessButton.classList.remove('d-none');
            }

            // Hide the More button if there are no more comments to load
            if (data.comments.length <= currentCommentCount + 3) {
                moreButton.classList.add('d-none');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Function to show fewer comments
function showLessComments(postId, currentUserId) {
    const commentsContainer = document.getElementById(`comments-${postId}`);
    const moreButton = document.getElementById(`more-button-${postId}`);
    const lessButton = document.getElementById(`less-button-${postId}`);

    // Fetch the initial 3 comments to show less
    fetch(`/comments/${postId}?limit=3`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            commentsContainer.innerHTML = '';

            data.comments.forEach(comment => {
                let editDeleteButtons = '';
                // Check if the current user is the author of the comment
                console.log("comment user id ",comment.user_id, "session user id",currentUserId);
                if (comment.user_id === currentUserId) {
                    editDeleteButtons = `
                        <div class="d-flex justify-content-end mt-2">
                            <a href="/edit_post/${comment.id}" class="btn btn-primary mr-2">Edit</a>
                            <form action="/delete_post/${comment.id}" method="POST" style="display: inline;">
                                <button type="submit" class="btn btn-danger" onclick="return confirm('Are you sure you want to delete this comment?')">Delete</button>
                            </form>
                        </div>
                    `;
                }
                const commentHtml = `
                    <div class="border p-3 mb-2">
                        <b>${comment.username}</b>: <strong>${comment.title}</strong><br>
                        <p class="mt-1">${comment.description}</p>
                        ${editDeleteButtons}
                    </div>
                `;
                commentsContainer.innerHTML += commentHtml;
            });

            // Show the More button again if we are back to the initial state
            moreButton.classList.remove('d-none');

            // Hide the Less button when only initial comments are displayed
            lessButton.classList.add('d-none');
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function vote(postId, voteType) {
    // Get the CSRF token from the body element
    const csrfToken = document.querySelector('body').dataset.csrfToken;

    // Send an AJAX request to vote
    fetch(`/vote/${postId}/${voteType}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update vote count and button styles based on the response
            const upvoteArrow = document.getElementById(`upvote-button-${postId}`);
            const downvoteArrow = document.getElementById(`downvote-button-${postId}`);
            const upvotesCount = document.getElementById(`upvotes-${postId}`);
            const downvotesCount = document.getElementById(`downvotes-${postId}`);

            // Verify elements before attempting to modify them
            if (upvoteArrow && downvoteArrow && upvotesCount && downvotesCount) {
                // Update vote counts
                upvotesCount.textContent = data.upvotes;
                downvotesCount.textContent = data.downvotes;

                // Change button styles to reflect vote state
                if (voteType === 'upvote') {
                    upvoteArrow.style.color = 'green';
                    downvoteArrow.style.color = 'red';
                } else if (voteType === 'downvote') {
                    downvoteArrow.style.color = 'red';
                    upvoteArrow.style.color = 'green';
                }
            } else {
                console.error('Vote elements not found in the DOM');
            }
        } else {
            console.error('Error in voting:', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function setupCountryCodeDropdown() {
    /*
    This function sets up the country code dropdown for the search page.
    */
    const countryCodeInput = document.getElementById('country-code-input');
    const countryCodeDropdown = document.getElementById('country-code-dropdown');

    // Event listener for filtering country code dropdown
    countryCodeInput.addEventListener('input', function () {
        filterDropdown(countryCodeInput, countryCodeDropdown);
    });

    // Event listener for selecting a country code from dropdown
    countryCodeDropdown.addEventListener('click', function (event) {
        selectDropdownItem(event, countryCodeInput, countryCodeDropdown);
    });

    // Event listener to move dropdown below the input when focused
    countryCodeInput.addEventListener('focus', function () {
        showDropdownBelowInput(countryCodeInput, countryCodeDropdown);
    });

    // Hide dropdown when the input loses focus after a slight delay to allow for clicks
    countryCodeInput.addEventListener('blur', function () {
        hideDropdownWithDelay(countryCodeDropdown);
    });
}

function setupPhoneNumberDropdown() {
    /*
    This function sets up the phone number dropdown for the search page.
    */
    const phoneNumberInput = document.getElementById('phone-number-input');
    const phoneNumberDropdown = document.getElementById('phone-number-dropdown');

    // Event listener for filtering phone number dropdown
    phoneNumberInput.addEventListener('input', function () {
        filterDropdown(phoneNumberInput, phoneNumberDropdown);
    });

    // Event listener for selecting a phone number from dropdown
    phoneNumberDropdown.addEventListener('click', function (event) {
        selectDropdownItem(event, phoneNumberInput, phoneNumberDropdown);
    });

    // Event listener for showing/hiding phone number dropdown
    phoneNumberInput.addEventListener('focus', function () {
        showDropdownBelowInput(phoneNumberInput, phoneNumberDropdown);
    });
    phoneNumberInput.addEventListener('blur', function () {
        hideDropdownWithDelay(phoneNumberDropdown);
    });
}

function setupSearchButton() {
    /*
    This function sets up the search button for the search page.
    */
    document.getElementById('search-button').addEventListener('click', function () {
        executeSearch();
    });
}

function filterDropdown(input, dropdown) {
    /*
    This function filters the dropdown items based on the input value.
    */
    const filter = input.value.toLowerCase();
    const items = dropdown.getElementsByTagName('li');
    let hasVisibleItems = false;
    // Loop through all items and show/hide based on the filter
    for (let item of items) {
        if (item.textContent.toLowerCase().includes(filter)) {
            item.style.display = '';
            hasVisibleItems = true;
        } else {
            item.style.display = 'none';
        }
    }

    // Show dropdown if there are items to show, otherwise hide it
    dropdown.classList.toggle('d-none', !hasVisibleItems);
}

function selectDropdownItem(event, input, dropdown) {
    /*
    This function selects an item from the dropdown and updates the input field.
    */
    if (event.target.tagName === 'LI') {
        input.value = event.target.getAttribute('data-value');
        dropdown.classList.add('d-none');
    }
}

function showDropdownBelowInput(input, dropdown) {
    /*
    This function shows the dropdown below the input field.
    */
    const rect = input.getBoundingClientRect();
    dropdown.style.top = `${rect.bottom / 4}px`;
    dropdown.classList.remove('d-none');
}

function hideDropdownWithDelay(dropdown) {
    /*
    This function hides the dropdown after a slight delay to allow for clicks.
    */

    setTimeout(() => {
        dropdown.classList.add('d-none');
    }, 200);
}

function executeSearch() {
    /*
    This function executes a search based on the country code and phone number input values.
    */
    const countryCodeInput = document.getElementById('country-code-input');
    const phoneNumberInput = document.getElementById('phone-number-input');
    const countryCode = countryCodeInput.value;
    const phoneNumber = phoneNumberInput.value;

    // Construct the search URL with query parameters
    let searchUrl = `/search?`;
    if (countryCode !== '') searchUrl += `country_code=${encodeURIComponent(countryCode)}&`;
    if (phoneNumber !== '') searchUrl += `phone_number=${encodeURIComponent(phoneNumber)}`;

    // Send AJAX request to search for posts
    fetch(searchUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        displaySearchResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displaySearchResults(data) {
    /*
    This function displays the search results on the search page.
    */
    const postsContainer = document.getElementById('posts-container');
    postsContainer.innerHTML = '';

    // Check if there are posts to display
    if (data.success && data.posts.length > 0) {
        const currentUserId = data.current_user_id;

        data.posts.forEach(post => {
            const postCard = createPostCard(post, currentUserId);
            postsContainer.innerHTML += postCard;
        });
    } else {
        postsContainer.innerHTML = '<p>No results found.</p>';
    }
}

function createPostCard(post, currentUserId) {
    /*
    This function creates an HTML card for a post with comments.
    */
    let commentsHtml = '';

    post.comments.forEach(comment => {
        let editDeleteButtons = '';

        // Check if the current user is the author of the comment
        if (comment.user_id === currentUserId) {
            editDeleteButtons = `
                <div class="d-flex justify-content-end mt-2">
                    <a href="/edit_post/${comment.id}" class="btn btn-primary mr-2">Edit</a>
                    <form action="/delete_post/${comment.id}" method="POST" style="display: inline;">
                        <button type="submit" class="btn btn-danger" onclick="return confirm('Are you sure you want to delete this comment?')">Delete</button>
                    </form>
                </div>
            `;
        }

        commentsHtml += `
            <div class="border p-3 mb-2">
                <b>${comment.username}</b>: <strong>${comment.title}</strong><br>
                <p class="mt-1">${comment.description}</p>
                ${editDeleteButtons}
            </div>
        `;
    });

    return `
        <div class="col-12 mb-4">
            <div class="card">
                <div class="card-header text-center d-flex align-items-center justify-content-between">
                    <div>
                        <h5 class="mb-0">${post.country_code} ${post.phone_number}</h5>
                    </div>
                    <div class="d-flex align-items-center">
                        <div class="mr-3 d-flex align-items-center">
                            <span id="upvotes-${post.id}">${post.upvotes}</span>
                            <button id="upvote-button-${post.id}" class="btn btn-link" style="color: green;" onclick="vote(${post.id}, 'upvote')">
                                &#9650;
                            </button>
                        </div>
                        <div class="d-flex align-items-center">
                            <span id="downvotes-${post.id}">${post.downvotes}</span>
                            <button id="downvote-button-${post.id}" class="btn btn-link" style="color: red;" onclick="vote(${post.id}, 'downvote')">
                                &#9660;
                            </button>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <h6 class="text-muted">Comments:</h6>
                    <div id="comments-${post.id}">
                        ${commentsHtml}
                    </div>
                    <!-- More/Less Comments Buttons -->
                    <button id="more-button-${post.id}" class="btn btn-link" onclick="showMoreComments(${post.id}, ${currentUserId})">More</button>
                    <button id="less-button-${post.id}" class="btn btn-link d-none" onclick="showLessComments(${post.id}, ${currentUserId})">Less</button>
                </div>
            </div>
        </div>
    `;
}
function setupCreatePostCountryCodeDropdown() {
    /*
    This function sets up the country code dropdown for the create post page.
    It listens for input events on the country code input field and filters country codes.
    It also listens for change events on the dropdown to update the input field with the selected country code.
    */
    const createPostCountryCodeInput = document.getElementById('country-code-input');
    const createPostCountryCodeDropdown = document.getElementById('country-code-dropdown');

    // Event listener for filtering country code dropdown
    createPostCountryCodeInput.addEventListener('input', function () {
        filterDropdown(createPostCountryCodeInput, createPostCountryCodeDropdown);
    });

    // Event listener for selecting a country code from dropdown
    createPostCountryCodeDropdown.addEventListener('click', function (event) {
        selectDropdownItem(event, createPostCountryCodeInput, createPostCountryCodeDropdown);
    });

    // Event listener to move dropdown below the input when focused
    createPostCountryCodeInput.addEventListener('focus', function () {
        showDropdownBelowInput(createPostCountryCodeInput, createPostCountryCodeDropdown);
    });

    // Hide dropdown when the input loses focus after a slight delay to allow for clicks
    createPostCountryCodeInput.addEventListener('blur', function () {
        hideDropdownWithDelay(createPostCountryCodeDropdown);
    });
}

// Assign functions to the global window object
window.filterDropdown = filterDropdown;
window.selectDropdownItem = selectDropdownItem;
window.showDropdownBelowInput = showDropdownBelowInput;
window.hideDropdownWithDelay = hideDropdownWithDelay;
window.setupCountryCodeDropdown = setupCountryCodeDropdown;
window.setupPhoneNumberDropdown = setupPhoneNumberDropdown;
window.setupSearchButton = setupSearchButton;
window.setupCreatePostCountryCodeDropdown = setupCreatePostCountryCodeDropdown;
window.vote = vote;


