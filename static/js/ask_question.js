// static/js/ask_question.js
// this file is used to handle the ask question form
// It includes the following features:
// 1. Category selection design
// 2. Random subject line placeholder 
// 3. Placeholders disappear when user starts typing
// 4. Tags: map category to a "locked" tag

// Category selection design. In the ask question form, the user can select a category by clicking on the image. The selected category will be highlighted and the value will be stored in the hidden input field.
console.log('ask_question.js loaded'); // passed test

document.addEventListener("DOMContentLoaded", (event) => {
    // Get all the radio inputs
    let options = document.querySelectorAll(
        '.standard-option input[type="radio"]'
    );
    console.log('options', options); // passed test
    console.log('options', options[0].value); // passed test

    // Add a click event listener to each radio input
    options.forEach((option) => {
        option.addEventListener("click", (e) => {
            // First reset all images to black and white and lowered position
            options.forEach((otherOption) => {
                let img = otherOption.nextElementSibling.querySelector(
                    ".card-img-top"
                );
                img.style.filter = "grayscale(70%)";
                img.style.transform = "translateY(30px)";
            });

            // Then color and raise the image of the selected radio
            let img = e.target.nextElementSibling.querySelector(
                ".card-img-top"
            );
            img.style.filter = "grayscale(0%)";
            img.style.transform = "translateY(0)";
            console.log('selected', e.target.value); // passed test
        });
    });
});


//random subject line placeholder goes inside the subject input field
document.addEventListener("DOMContentLoaded", (event) => {
    console.log('random subject line placeholder'); // passed test
    const prompts = [
        "struggling to implement differentiation into my mathematics lesson",
        "How could I prepare my art lessons more effectively with 1 technician available?",
        "How can I handle a professional conversation about marking workload?",
        "How can I set consistently high expectations for all students in a diverse classroom?",
        "What strategies can be used to motivate students who struggle with self-confidence?",
        "What are effective methods to challenge high-achieving students in a mixed-ability class?",
        "How can I track student progress in real-time during lessons?",
        "What techniques can help identify when a student is about to fall behind?",
        "How can peer-assessment be used to promote progress in a collaborative project?",
        "How can I stay updated with the latest developments in my subject area?",
        "What are some creative ways to integrate interdisciplinary knowledge into a subject?",
        "What role does technology play in enhancing subject knowledge for students?",
        "How can I plan lessons to accommodate unexpected disruptions?",
        "What are some time-saving tips for lesson planning without sacrificing quality?",
        "How could I prepare my art lessons more effectively with 1 technician available?",
        "What are practical approaches to differentiate instruction in a large class?",
        "How can technology be leveraged for differentiated learning paths?",
        "Struggling to implement differentiation into my mathematics lesson.",
        "How can I design assessments that give meaningful feedback to each student?",
        "What are the pros and cons of formative vs. summative assessments?",
        "How can I handle a professional conversation about marking workload?",
        "What classroom management techniques are effective without stifling creativity?",
        "How can I ensure a fair behavior policy that adapts to individual student needs?",
        "How can I turn challenging behavior into a learning opportunity for the whole class?",
        "What are some strategies for maintaining a work-life balance as a teacher?",
        "How can I foster a culture of continuous professional development among staff?",
        "What is the role of reflective practice in personal and professional growth as an educator?"
    ];

    const subjectInput = document.getElementById("id_subject");
    const randomPrompt = prompts[Math.floor(Math.random() * prompts.length)];
    subjectInput.placeholder =
        "Enter your subject line here e.g. " + randomPrompt;
}); // seems to work as expected

console.log('test interim');

// ******************** above code has been tested and works as expected ******************** //

console.log('Adding event listener to .tag-input input');
const tagInputEl = document.querySelector(".tag-input input");
if (tagInputEl) {
  tagInputEl.addEventListener("keyup", addTag);
} else {
  console.error('.tag-input input not found'); // returns, thereby failing the test
}

console.log('Initializing Quill editor');
const quillEditorEl = document.querySelector('#quill-editor');
if (quillEditorEl) {
  var quill = new Quill(quillEditorEl, { theme: 'snow' });
  // ... rest of Quill setup code
} else {
  console.error('#quill-editor not found'); // returns, thereby failing the test
}

//text placeholder disappears when user starts typing
document.addEventListener("DOMContentLoaded", (event) => {
    console.log('text placeholder disappears when user starts typing'); // failed test
    const contentArea = document.getElementById("id_content");
    contentArea.addEventListener(
        "focus",
        function () {
            if (this.defaultValue === this.value) {
                this.value = "";
                console.log('placeholder removed');
            }
        }, {
            once: true
        }
    ); // The event will only trigger once
});

// quill editor
var quill = new Quill('#quill-editor', {
    theme: 'snow'
});

console.log('quill', quill); // failed test


// Listen for text change in the Quill editor
quill.on('text-change', updateContent);