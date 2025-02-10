document.addEventListener("DOMContentLoaded", async () => {
    const sectionTitle = document.getElementById("section-title");
    const contentPlaceholder = document.querySelector(".content-placeholder");
    const prevBtn = document.getElementById("prev-btn");
    const nextBtn = document.getElementById("next-btn");

    let currentSection = 0;
    let sections = [];

    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    const courseId = getQueryParam("course_id");
    if (!courseId) {
        sectionTitle.textContent = "Course Not Found";
        return;
    }

    async function fetchLessons() {
        try {
            const response = await fetch(`/get_lessons?course_id=${courseId}`);
            const data = await response.json();
            if (data.length === 0) {
                sectionTitle.textContent = "No Lessons Available";
                return;
            }

            sections = data;
            updateContent();
        } catch (error) {
            console.error("Error fetching lessons:", error);
            sectionTitle.textContent = "Error loading lessons";
        }
    }

    function updateContent() {
        if (sections.length === 0) return;
        sectionTitle.textContent = sections[currentSection].title;
        contentPlaceholder.innerHTML = `<div class="line">${sections[currentSection].content}</div>`;
    }

    prevBtn.addEventListener("click", () => {
        if (currentSection > 0) {
            currentSection--;
            updateContent();
        }
    });

    nextBtn.addEventListener("click", () => {
        if (currentSection < sections.length - 1) {
            currentSection++;
            updateContent();
        }
    });

    fetchLessons();
});
