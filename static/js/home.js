/* =========================================================
   KOHINOOR — HOMEPAGE INTERACTIONS
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  const productGrid = document.getElementById("homeProductGrid");

  if (!productGrid) return;

  const cards = Array.from(
    productGrid.querySelectorAll("[data-product-card]")
  );

  const filterButtons = Array.from(
    document.querySelectorAll(".kh-filter-button")
  );

  const searchInput = document.getElementById("homeProductSearch");
  const noProducts = document.getElementById("homeNoProducts");
  const clearButton = document.getElementById("clearHomeFilters");

  let activeFilter = "all";
  let searchTerm = "";


  function filterProducts() {

    let visibleCount = 0;

    cards.forEach(card => {

      const category = (
        card.dataset.category || ""
      ).toLowerCase();

      const cardText = (
        card.textContent || ""
      ).toLowerCase();

      const matchesCategory =
        activeFilter === "all" ||
        category === activeFilter;

      const matchesSearch =
        !searchTerm ||
        cardText.includes(searchTerm);

      const shouldShow =
        matchesCategory && matchesSearch;

      card.hidden = !shouldShow;

      if (shouldShow) {
        visibleCount++;
      }

    });

    if (noProducts) {
      noProducts.hidden = visibleCount !== 0;
    }

  }


  filterButtons.forEach(button => {

    button.addEventListener("click", () => {

      activeFilter = (
        button.dataset.filter || "all"
      ).toLowerCase();

      filterButtons.forEach(item => {
        item.classList.remove("active");
        item.setAttribute("aria-pressed", "false");
      });

      button.classList.add("active");
      button.setAttribute("aria-pressed", "true");

      filterProducts();

    });

    button.setAttribute(
      "aria-pressed",
      button.classList.contains("active") ? "true" : "false"
    );

  });


  if (searchInput) {

    searchInput.addEventListener("input", event => {

      searchTerm = event.target.value
        .trim()
        .toLowerCase();

      filterProducts();

    });

  }


  if (clearButton) {

    clearButton.addEventListener("click", () => {

      activeFilter = "all";
      searchTerm = "";

      if (searchInput) {
        searchInput.value = "";
      }

      filterButtons.forEach(button => {

        const isAll =
          button.dataset.filter === "all";

        button.classList.toggle("active", isAll);

        button.setAttribute(
          "aria-pressed",
          isAll ? "true" : "false"
        );

      });

      filterProducts();

    });

  }


  filterProducts();

});