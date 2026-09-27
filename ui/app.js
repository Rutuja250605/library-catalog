// Update this once the API Service is deployed and you know its address.
const API_BASE = "http://localhost:8000";

async function loadBooks() {
  const res = await fetch(`${API_BASE}/books`);
  const books = await res.json();
  const list = document.getElementById("book-list");
  list.innerHTML = "";
  books.forEach(b => {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${b.title}</td><td>${b.author}</td><td>${b.year}</td>`;
    list.appendChild(row);
  });
}

document.getElementById("book-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const book = {
    title: document.getElementById("title").value,
    author: document.getElementById("author").value,
    year: parseInt(document.getElementById("year").value)
  };
  await fetch(`${API_BASE}/books`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(book)
  });
  e.target.reset();
  loadBooks();
});

loadBooks();