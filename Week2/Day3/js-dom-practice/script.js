const accordions = document.querySelectorAll(".accordion");

accordions.forEach(acc => {
  const header = acc.querySelector(".accordion-header");
  const body = acc.querySelector(".accordion-body");
  const icon = acc.querySelector(".icon");

  header.addEventListener("click", () => {
    
    // Close all others before opening a new one
    accordions.forEach(item => {
      if (item !== acc) {
        item.querySelector(".accordion-body").classList.remove("open");
        item.querySelector(".icon").textContent = "+";
      }
    });

    // Toggle current one
    body.classList.toggle("open");

    // Icon change
    icon.textContent = body.classList.contains("open") ? "−" : "+";
  });
});
