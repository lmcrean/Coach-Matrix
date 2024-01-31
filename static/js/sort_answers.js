function sortAnswers(sortType) {
    console.log("Sort Type selected: ", sortType); // Debugging log

    // Construct the URL with the new sort parameter
    const url = new URL(window.location);
    url.searchParams.set('sort_by', sortType);

    console.log("URL being set: ", url.toString()); // Debugging log

    // Redirect to the new URL
    window.location.href = url.toString();
}
