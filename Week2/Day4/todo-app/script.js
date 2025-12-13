let todos = JSON.parse(localStorage.getItem("todos")) || [];

// Save to LocalStorage
function saveTodos() {
  localStorage.setItem("todos", JSON.stringify(todos));
}

// Render todo list
function render() {
  const list = document.getElementById("todo-list");
  list.innerHTML = "";

  todos.forEach((todo, index) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span>${todo}</span>
      <button onclick="edit(${index})">Edit</button>
      <button onclick="remove(${index})">Delete</button>
    `;
    list.appendChild(li);
  });
}

render();

// Add todo
document.getElementById("add-btn").addEventListener("click", () => {
  const input = document.getElementById("todo-input");
  const value = input.value.trim();

  if (!value) return;

  todos.push(value);
  saveTodos();
  render();
  input.value = "";
});

// Edit todo
function edit(index) {
  const updated = prompt("Edit task:", todos[index]);
  if (updated) {
    todos[index] = updated;
    saveTodos();
    render();
  }
}

// Delete todo
function remove(index) {
  todos.splice(index, 1);
  saveTodos();
  render();
}
