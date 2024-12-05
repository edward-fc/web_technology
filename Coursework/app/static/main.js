document.addEventListener('DOMContentLoaded', function () {
    // Call the function to set up the country code dropdown for the create post page
    window.setupCountryCodeDropdown();
    // Call the function to set up the phone number dropdown for the create post page
    window.setupPhoneNumberDropdown();
    // Call the function to set up the search button for the search page
    window.setupSearchButton();
    // Call the function to make it the user can vote only once
    window.vote();
});
