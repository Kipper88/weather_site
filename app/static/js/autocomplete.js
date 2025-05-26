document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("city-input");
    const list = document.getElementById("autocomplete-list");
    let timeoutId;

    function clearList() {
        list.innerHTML = "";
        list.classList.add("hidden");
        input.setAttribute("aria-expanded", "false");
    }

    function fillList(cities) {
        clearList();
        if (!cities.length) return;

        for (const city of cities) {
            const item = document.createElement("li");
            item.className = "cursor-pointer px-3 py-2 hover:bg-blue-600";

            item.textContent = city.name;
            item.tabIndex = 0;

            item.addEventListener("click", () => {
                input.value = item.textContent;
                clearList();
            });

            item.addEventListener("keydown", (e) => {
                if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    input.value = item.textContent;
                    clearList();
                    input.focus();
                }
            });

            list.appendChild(item);
        }
        list.classList.remove("hidden");
        input.setAttribute("aria-expanded", "true");
    }

    input.addEventListener("input", () => {
        clearTimeout(timeoutId);
        const query = input.value.trim();
        if (query.length < 2) {
            clearList();
            return;
        }
        timeoutId = setTimeout(() => {
            fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(query)}&count=5&language=ru&format=json`)
                .then(response => response.json())
                .then(data => {
                    if (!data.results) {
                        clearList();
                        return;
                    }
                    fillList(data.results);
                })
                .catch(() => {
                    clearList();
                });
        }, 300);
    });

    document.addEventListener("click", (e) => {
        if (!input.contains(e.target) && !list.contains(e.target)) {
            clearList();
        }
    });
});