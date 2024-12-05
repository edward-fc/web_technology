
// Listen for the DOMContentLoaded event, then run the function
document.addEventListener('DOMContentLoaded', function () {
    // Call the function to set up the country code dropdown for the create post page
    setupCreatePostCountryCodeDropdown();
});

function setupCreatePostCountryCodeDropdown() {
    /*
    This function sets up the country code dropdown for the create post page.
    It listens for input events on the country code input field and makes an AJAX request to filter country codes.
    It also listens for change events on the dropdown to update the input field with the selected country code.
    */
   // select the input and dropdown elements
    const createPostCountryCodeInput = document.getElementById('country-code-input');
    const createPostCountryCodeDropdown = document.getElementById('country-code-dropdown');

    // Event listener for filtering country code dropdown via AJAX
    createPostCountryCodeInput.addEventListener('input', function () {
        const query = createPostCountryCodeInput.value;

        if (query.length > 0) {
            // Make an AJAX request to filter country codes
            fetch(`/filter_country_codes?query=${encodeURIComponent(query)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        updateCountryCodeSelect(data.country_codes, createPostCountryCodeDropdown);
                    }
                })
                .catch(error => {
                    console.error('Error fetching country codes:', error);
                });
        } else {
            // Clear the dropdown if the input is empty
            createPostCountryCodeDropdown.innerHTML = '';
            createPostCountryCodeDropdown.classList.add('d-none');
        }
    });
    // Event listener for selecting a country code from dropdown using click
    document.addEventListener('change', function (event) {
        // Check if the target element has id 'country-code-dropdown'
        if (event.target && event.target.id === 'country-code-input') {
            // Update the input value with the selected country code
            createPostCountryCodeInput.value = createPostCountryCodeDropdown.value;
            createPostCountryCodeDropdown.classList.add('d-none');
        }
    });
}

// Function to update the country code dropdown (select element) with new data
function updateCountryCodeSelect(countryCodes, dropdown) {
    /*
    This function updates the country code dropdown with the given data.
    It clears the dropdown and adds new options based on the country codes provided.
    */
    dropdown.innerHTML = '';
    // Loop through the country codes and create an option element for each
    countryCodes.forEach(country => {
        const option = document.createElement('option');
        option.value = country.code;
        option.textContent = `${country.name} (${country.code})`;
        dropdown.appendChild(option);
    });

    dropdown.classList.remove('d-none');
}
