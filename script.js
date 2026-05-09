// ---------- SAMPLE DATA ----------
let items = [
    {
      id: 1,
      name: "Parle-G Biscuits",
      cat: "Snacks",
      qty: "1 Pack",
      expiry: "2026-05-20",
      fridge: false
    },
    {
      id: 2,
      name: "Milk",
      cat: "Dairy",
      qty: "1 L",
      expiry: "2026-05-12",
      fridge: true
    },
    {
      id: 3,
      name: "Bananas",
      cat: "Fruits",
      qty: "6 pcs",
      expiry: "2026-05-11",
      fridge: false
    }
  ];
  
  let nextId = 4;
  let activeFilter = "all";
  
  // ---------- CATEGORY ICONS ----------
  const categoryIcons = {
    Snacks: "🍪",
    Dairy: "🥛",
    Fruits: "🍎",
    Vegetables: "🥬",
    Beverages: "🧃",
    Other: "📦"
  };
  
  // ---------- DATE HELPERS ----------
  function daysLeft(expiry) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
  
    const exp = new Date(expiry);
    exp.setHours(0, 0, 0, 0);
  
    return Math.round((exp - today) / 86400000);
  }
  
  function freshness(days) {
    if (days < 0) return "r";
    if (days <= 3) return "a";
    return "g";
  }
  
  function label(days) {
    if (days < 0) return `Expired ${Math.abs(days)}d ago`;
    if (days === 0) return "Expires today";
    return `${days}d left`;
  }
  
  // ---------- ITEM CARD ----------
  function itemCard(item) {
    const days = daysLeft(item.expiry);
    const status = freshness(days);
    const icon = categoryIcons[item.cat] || "📦";
  
    return `
      <div class="item-card">
        <div class="item-icon ${status}">${icon}</div>
  
        <div class="item-info">
          <div class="item-name">${item.name}</div>
          <div class="item-meta">${item.cat} • ${item.qty}</div>
        </div>
  
        <span class="badge ${status}">
          ${label(days)}
        </span>
  
        <button class="btn-del" onclick="deleteItem(${item.id})">
          ✕
        </button>
      </div>
    `;
  }
  
  // ---------- STATS ----------
  function updateStats() {
    const total = items.length;
    const fresh = items.filter(i => freshness(daysLeft(i.expiry)) === "g").length;
    const expiring = items.filter(i => freshness(daysLeft(i.expiry)) === "a").length;
    const expired = items.filter(i => freshness(daysLeft(i.expiry)) === "r").length;
  
    document.getElementById("s-total").textContent = total;
    document.getElementById("s-g").textContent = fresh;
    document.getElementById("s-a").textContent = expiring;
    document.getElementById("s-r").textContent = expired;
  
    // Fridge stats
    const fridgeItems = items.filter(i => i.fridge);
    document.getElementById("sf-total").textContent = fridgeItems.length;
    document.getElementById("sf-g").textContent =
      fridgeItems.filter(i => freshness(daysLeft(i.expiry)) === "g").length;
    document.getElementById("sf-a").textContent =
      fridgeItems.filter(i => freshness(daysLeft(i.expiry)) === "a").length;
    document.getElementById("sf-r").textContent =
      fridgeItems.filter(i => freshness(daysLeft(i.expiry)) === "r").length;
  }
  
  // ---------- INVENTORY ----------
  function renderInv() {
    const search = document.getElementById("search").value.toLowerCase();
  
    const filtered = items.filter(item => {
      const status = freshness(daysLeft(item.expiry));
  
      const matchesFilter =
        activeFilter === "all" || status === activeFilter;
  
      const matchesSearch =
        item.name.toLowerCase().includes(search) ||
        item.cat.toLowerCase().includes(search);
  
      return matchesFilter && matchesSearch;
    });
  
    const container = document.getElementById("inv-list");
  
    if (filtered.length === 0) {
      container.innerHTML = '<div class="empty">No items found</div>';
    } else {
      container.innerHTML = filtered.map(itemCard).join("");
    }
  
    updateStats();
  }
  
  // ---------- MY FRIDGE ----------
  function renderFridge() {
    const fridgeItems = items.filter(i => i.fridge);
    const container = document.getElementById("fridge-list");
  
    if (fridgeItems.length === 0) {
      container.innerHTML =
        '<div class="fridge-empty">❄️ No items in fridge</div>';
    } else {
      container.innerHTML = fridgeItems.map(itemCard).join("");
    }
  }
  
  // ---------- CATEGORIES ----------
  function renderCats() {
    const groups = {};
  
    items.forEach(item => {
      if (!groups[item.cat]) groups[item.cat] = [];
      groups[item.cat].push(item);
    });
  
    const container = document.getElementById("cat-body");
    let html = "";
  
    for (const cat in groups) {
      html += `
        <div style="margin-bottom:40px;">
          <h2 style="margin-bottom:18px;">
            ${categoryIcons[cat] || "📦"} ${cat}
          </h2>
          <div class="items">
            ${groups[cat].map(itemCard).join("")}
          </div>
        </div>
      `;
    }
  
    container.innerHTML = html || '<div class="empty">No items</div>';
  }
  
  // ---------- ALERTS ----------
  function renderAlerts() {
    const urgent = items.filter(i => daysLeft(i.expiry) <= 3);
    const container = document.getElementById("alert-list");
  
    if (urgent.length === 0) {
      container.innerHTML =
        '<div class="empty">✅ No urgent alerts</div>';
      return;
    }
  
    container.innerHTML = urgent.map(itemCard).join("");
  }
  
  // ---------- RECIPES ----------
  function renderRecipes() {
    document.getElementById("recipe-list").innerHTML = `
      <div class="item-card">
        <div class="item-info">
          <div class="item-name">🍳 Banana Smoothie</div>
          <div class="item-meta">
            Uses bananas, milk and yogurt.
          </div>
        </div>
      </div>
  
      <div class="item-card">
        <div class="item-info">
          <div class="item-name">🥗 Fruit Salad</div>
          <div class="item-meta">
            Uses bananas and other fruits.
          </div>
        </div>
      </div>
    `;
  }
  
  // ---------- FILTER ----------
  function setFilter(filter) {
    activeFilter = filter;
  
    document.querySelectorAll(".pill").forEach(p =>
      p.className = "pill"
    );
  
    if (filter === "all") {
      document.getElementById("p-all").classList.add("f-all");
    }
  
    renderInv();
  }
  
  // ---------- DELETE ----------
  function deleteItem(id) {
    items = items.filter(item => item.id !== id);
    renderAll();
  }
  
  // ---------- MODAL ----------
  function openModal() {
    document.getElementById("modal").classList.add("open");
  }
  
  function closeModal() {
    document.getElementById("modal").classList.remove("open");
  
    document.getElementById("f-name").value = "";
    document.getElementById("f-qty").value = "";
  }
  
  // ---------- SAVE ITEM ----------
  function saveItem() {
    const name = document.getElementById("f-name").value.trim();
    const cat = document.getElementById("f-cat").value;
    const expiry = document.getElementById("f-expiry").value;
    const qty =
      document.getElementById("f-qty").value.trim() || "1";
  
    if (!name || !expiry) {
      alert("Please enter item name and expiry date.");
      return;
    }
  
    items.unshift({
      id: nextId++,
      name,
      cat,
      qty,
      expiry,
      fridge: false
    });
  
    closeModal();
    renderAll();
  }
  
  // ---------- TAB NAVIGATION ----------
  function go(tab) {
    document
      .querySelectorAll(".section")
      .forEach(sec => sec.classList.remove("active"));
  
    document
      .querySelectorAll(".nav-tab")
      .forEach(tabEl => tabEl.classList.remove("active"));
  
    document
      .getElementById("sec-" + tab)
      .classList.add("active");
  
    const tabs = ["inv", "fridge", "cats", "alerts", "recipes"];
    document
      .querySelectorAll(".nav-tab")
      [tabs.indexOf(tab)]
      .classList.add("active");
  }
  
  // ---------- RENDER ALL ----------
  function renderAll() {
    renderInv();
    renderFridge();
    renderCats();
    renderAlerts();
    renderRecipes();
  }
  
  // ---------- CLOSE MODAL ON BACKGROUND CLICK ----------
  document.getElementById("modal").addEventListener("click", function (e) {
    if (e.target === this) {
      closeModal();
    }
  });
  function toggleTheme() {
    const body = document.body;
    const isDark = body.classList.toggle('dark');
  
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  
    const btn = document.querySelector('.theme-toggle');
    if (btn) {
      btn.textContent = isDark ? '☀️' : '🌙';
    }
  }
  
  function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    const btn = document.querySelector('.theme-toggle');
  
    if (savedTheme === 'dark') {
      document.body.classList.add('dark');
      if (btn) btn.textContent = '☀️';
    } else {
      document.body.classList.remove('dark');
      if (btn) btn.textContent = '🌙';
    }
  }
  
  // ---------- INITIAL LOAD ----------
  loadTheme();
  renderAll();
