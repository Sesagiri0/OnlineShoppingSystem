// ShopEase — small client-side niceties (no external libraries required)

document.addEventListener("DOMContentLoaded", function () {
  // Auto-dismiss flash messages after 4 seconds
  document.querySelectorAll(".flash").forEach(function (el) {
    setTimeout(function () {
      el.style.transition = "opacity 0.5s ease";
      el.style.opacity = "0";
      setTimeout(function () { el.remove(); }, 500);
    }, 4000);
  });

  // Confirm before deleting a product/category from the admin panel
  document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!confirm(form.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });
});
