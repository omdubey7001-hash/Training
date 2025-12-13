document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("product-container");
  const searchInput = document.getElementById("search");
  const sortSelect = document.getElementById("sort");

  let products = [];
  let filteredProducts = [];

  async function loadProducts() {
    try {
      const res = await fetch("https://dummyjson.com/products");
      const data = await res.json();
      products = data.products;
      filteredProducts = products;
      renderProducts(products);
    } catch (err) {
      console.log("Error loading products:", err);
      container.innerHTML = "<h2 style='color:red'>Failed to load products</h2>";
    }
  }

  loadProducts();

  function renderProducts(list) {
    container.innerHTML = "";
    list.forEach(product => {
      container.innerHTML += `
        <div class="card">
          <img src="${product.thumbnail}" alt="${product.title}">
          <h3>${product.title}</h3>
          <p>$${product.price}</p>
        </div>
      `;
    });
  }

  // Search
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    filteredProducts = products.filter(p =>
      p.title.toLowerCase().includes(query)
    );
    renderProducts(filteredProducts);
  });

  // Sort
  sortSelect.addEventListener("change", () => {
    if (sortSelect.value === "low") {
      filteredProducts.sort((a, b) => a.price - b.price);
    } else if (sortSelect.value === "high") {
      filteredProducts.sort((a, b) => b.price - a.price);
    }
    renderProducts(filteredProducts);
  });
});
