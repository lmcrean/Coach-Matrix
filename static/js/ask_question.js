// static/js/ask_question.js
// this file is used to handle the ask question form
// It includes the following features:
// 1. Random subject line placeholder 


//random subject line placeholder goes inside the subject input field
document.addEventListener("DOMContentLoaded", (event) => {
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
}); 