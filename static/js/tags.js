// tags.js

// this file is for handling the tags input in ask_question.html

// it connects to the {{ form.tags | as_crispy_field }} field in the form which appears as like this when rendered in HTML:
    // <input type="text" name="tags" class="textinput textInput form-control" id="id_tags">


// 1. Tags: map category to a "locked" tag, update when the user selects a category:
    // 1.1 Add event listener for the radio buttons
    // 1.2. When the user selects a radio button, show the corresponding input field as a locked input

// 2. Tags: Create, read, update and delete the tags in the input with validation:
    // 2.1 Add event listener for keyup event on the tag input
    // 2.2 When the user presses enter or space, add the tag to the list
    // 2.3 If the tag is already used, show an error message

console.log('Starting tags.js script');


// 1. Tags: map category to a "locked" tag
document.addEventListener

("DOMContentLoaded", (event) => {
    console.log('tags: map category to a "locked" tag'); // failed test

    // Object mapping radio button values to tags
    const tagsMap = {
        1: "high_expectations",
        2: "promoting_progress",
        3: "subject_knowledge",
        4: "planning",
        5: "differentiation",
        6: "assessment",
        7: "behaviour_management",
        8: "professionalism"
    };

    // Function to update the tag list
    function updateTag(selectedValue) {
        console.log('selectedValue', selectedValue); // failed test
        // Get the tag list and locked tag elements
        const tagList = document.querySelector(".tag-list");
        const lockedTag = document.querySelector(".tag.locked");
        console.log('tagList', tagList); // failed test
        console.log('lockedTag', lockedTag); // failed test

        // Create a new locked tag only if it doesn't exist
        if (!lockedTag) {
            console.log('creating new locked tag'); // failed test
            const tag = document.createElement("span");
            tag.className = "tag badge badge-secondary locked"; // Include Bootstrap classes for consistent styling
            tag.textContent = tagsMap[selectedValue];
            // Add a Font Awesome lock icon to the tag
            const lockIcon = document.createElement("i");
            lockIcon.className = "fas fa-lock mr-2"; // 'mr-2' for a little space between icon and text
            tag.prepend(lockIcon); // Add the lock icon before the tag text

            // Append the new locked tag to the tag list
            tagList.appendChild(tag);
        } else {
            console.log('updating existing locked tag'); // failed test
            // Update the text and value of the existing locked tag
            lockedTag.textContent = tagsMap[selectedValue];
            const lockIcon = document.createElement("i");
            lockIcon.className = "fas fa-lock mr-2";
            lockedTag.prepend(lockIcon);
        }
    }

    // Attach event listeners to radio buttons
    const standardOptions = document.querySelectorAll(
        '.standard-option input[type="radio"]'
    );
    console.log('standardOptions', standardOptions);
    standardOptions.forEach((option) => { // this is for each radio button
        option.addEventListener("change", (e) => { // when the radio button is changed
            updateTag(e.target.value); // update the tag
            console.log('e.target.value', e.target.value);
        });
    });
    c
});


// 2. tags: standard input

let tags = [];

console.log('tags', tags);

function addTag(e) {
    console.log('addTag'); // failed test
    let code = e.keyCode ? e.keyCode : e.which;
    let errorElement = document.getElementById("tag-error");
    errorElement.style.display = "none"; // Hide error initially
    if (code === 13 || code === 32) {
        console.log('enter key or space bar pressed'); // failed test
        // Enter key or Space bar
        e.preventDefault(); // Prevent default form submission
        e.stopPropagation(); // Stop event from propagating to parent elements

        let tag = e.target.value.trim();

        //Validation: only 5 tags
        if (tags.length >= 5) {
            showError("Only 5 tags can be added.");
            tagInput.value = "";
            return;
        }

        // Validation: Check if tag is empty or already exists
        if (!tag || tag.length < 1 || tags.includes(tag)) {
            showError("Tag cannot be empty or already used");
            e.target.value = "";
            return;
        }

        // Validation: Allow only letters, numbers, hyphens, and underscores
        if (!/^[A-Za-z0-9-_]+$/.test(tag)) {
            showError(
                "Tags can only contain letters, numbers, hyphens, and underscores."
            );
            e.target.value = "";
            return;
        }

        // Check tag length max 20 characters
        if (tag.length > 20) {
            showError("Tags should not be longer than 20 characters.");
            e.target.value = "";
            return;
        }

        tags.push(tag);

        let tagItem = document.createElement("div");
        tagItem.classList.add("item");
        tagItem.innerHTML = `
            <span class="delete-btn" onclick="deleteTag(this, '${tag}')">
                &times;
            </span>
            <span>${tag}</span>
        `;
        document.querySelector(".tag-input .tag-list").appendChild(tagItem);
        e.target.value = "";
    }
}

function deleteTag(ref, tag) {
    // Remove the tag from the array and the DOM
    console.log('deleteTag'); // failed test
    let parent = ref.parentNode.parentNode;
    parent.removeChild(ref.parentNode);
    let index = tags.indexOf(tag);
    tags.splice(index, 1);
}

function showError(message) {
    // Display error message
    console.log('showError'); // failed test
    let errorElement = document.getElementById("tag-error");
    errorElement.textContent = message;
    errorElement.style.display = "block";
}

document.querySelector(".tag-input input").addEventListener("keyup", addTag);

console.log('tags', tags);

// quill editor
var quill = new Quill('#quill-editor', {
    theme: 'snow'
});

console.log('quill', quill); // failed test

// Function to update hidden textarea with Quill content
function updateContent() {
    console.log('updateContent'); // failed test
    var content = document.querySelector('#quill-content');
    content.value = JSON.stringify(quill.getContents());
    console.log('content', content.value); // failed test
}

// Listen for text change in the Quill editor
quill.on('text-change', updateContent);

document.getElementById('standards-form').addEventListener('submit', updateContent);