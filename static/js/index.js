document.addEventListener("DOMContentLoaded", () => {
  const bookmarkBtn = document.getElementById("bookmarkBtn");
  const savedWordsList = document.getElementById("savedWordsList");
  let currentWord = bookmarkBtn ? bookmarkBtn.dataset.word : null;

  // Load saved words and mark current word if saved
  const loadSavedWords = () => {
    const saved = JSON.parse(localStorage.getItem("savedWords") || "[]");
    if (!savedWordsList) return;

    savedWordsList.innerHTML = "";

    saved.forEach((word) => {
      const li = document.createElement("li");
      li.textContent = word;

      li.addEventListener("click", () => {
        postWord(word);
      });

      savedWordsList.appendChild(li);
    });

    // Update bookmark button state
    if (bookmarkBtn && currentWord) {
      if (saved.includes(currentWord)) {
        bookmarkBtn.textContent = "★ Saved";
        bookmarkBtn.style.background = "#b7e4c7";
        bookmarkBtn.dataset.saved = "true";
      } else {
        bookmarkBtn.textContent = "☆ Bookmark";
        bookmarkBtn.style.background = "#fff";
        bookmarkBtn.dataset.saved = "false";
      }
    }
  };

  loadSavedWords();

  // Toggle save/unsave
  if (bookmarkBtn && currentWord) {
    bookmarkBtn.addEventListener("click", () => {
      let saved = JSON.parse(localStorage.getItem("savedWords") || "[]");
      const index = saved.indexOf(currentWord);

      if (index === -1) {
        // Save
        saved.push(currentWord);
        bookmarkBtn.textContent = "★ Saved";
        bookmarkBtn.style.background = "#b7e4c7";
        bookmarkBtn.dataset.saved = "true";
      } else {
        // Un-save
        saved.splice(index, 1);
        bookmarkBtn.textContent = "☆ Bookmark";
        bookmarkBtn.style.background = "#fff";
        bookmarkBtn.dataset.saved = "false";
      }

      localStorage.setItem("savedWords", JSON.stringify(saved));
      loadSavedWords();
    });
  }

  // Function to POST/GET word and update definitions
  function postWord(word) {
    fetch("/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ word }),
    })
      .then((res) => res.text())
      .then((html) => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");

        const newEn = doc.querySelector(".en-section");
        const newAmh = doc.querySelector(".amh-section");

        const enSection = document.querySelector(".en-section");
        const amhSection = document.querySelector(".amh-section");

        if (enSection && newEn) enSection.innerHTML = newEn.innerHTML;
        if (amhSection && newAmh) amhSection.innerHTML = newAmh.innerHTML;

        // update currentWord and dataset
        currentWord = word;
        if (bookmarkBtn) bookmarkBtn.dataset.word = word;

        // UPDATE FORM INPUT
        const formInput = document.querySelector('input[name="word"]');
        if (formInput) formInput.value = word;

        loadSavedWords();
      })
      .catch(console.error);
  }
});
