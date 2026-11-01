// Small enhancements; every page works without them except zoom and copy.

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

function toast(text) {
  const box = $(".toast");
  if (!box) return;
  box.textContent = text;
  window.setTimeout(() => { box.textContent = ""; }, 4000);
}

// Bind each element once, however often setup runs after htmx swaps.
function once(el, name) {
  const key = `bound${name}`;
  if (el.dataset[key]) return false;
  el.dataset[key] = "1";
  return true;
}

document.documentElement.classList.add("js");

function setup(root = document) {
  // Zoom the paper: buttons and keyboard (+, -, 0) on the viewer.
  const canvas = $("[data-canvas]", root);
  if (canvas && once(canvas, "Zoom")) {
    let zoom = 1;
    const apply = () => { canvas.style.width = `${Math.round(zoom * 100)}%`; };
    const change = (kind) => {
      if (kind === "in") zoom = Math.min(4, zoom * 1.25);
      else if (kind === "out") zoom = Math.max(1, zoom / 1.25);
      else zoom = 1;
      apply();
    };
    $$("[data-zoom]", root).forEach((button) => {
      button.addEventListener("click", () => change(button.dataset.zoom));
    });
    const frame = $("[data-viewer]", root);
    frame?.addEventListener("keydown", (event) => {
      if (event.key === "+" || event.key === "=") change("in");
      else if (event.key === "-") change("out");
      else if (event.key === "0") change("fit");
    });
  }

  // Selecting a box selects its row and the other way round.
  const select = (id) => {
    $$(".is-selected[data-claim]", root).forEach((el) => el.classList.remove("is-selected"));
    $$(`[data-claim="${CSS.escape(id)}"]`, root).forEach((el) => el.classList.add("is-selected"));
  };
  $$("a.box[data-claim]", root).filter((el) => once(el, "Select")).forEach((box) => {
    box.addEventListener("click", () => select(box.dataset.claim));
  });
  $$("tr.row[data-claim]", root).filter((el) => once(el, "Select")).forEach((row) => {
    row.addEventListener("click", () => select(row.dataset.claim));
  });

  // Arrow keys move between rows of the claims table; Escape closes an open edit.
  const rows = $$("tr.row[data-claim]", root);
  rows.forEach((row, index) => {
    if (!once(row, "Keys")) return;
    row.addEventListener("keydown", (event) => {
      if (event.target !== row) return;
      if (event.key === "ArrowDown" && rows[index + 1]) { rows[index + 1].focus(); event.preventDefault(); }
      if (event.key === "ArrowUp" && rows[index - 1]) { rows[index - 1].focus(); event.preventDefault(); }
      if (event.key === "Enter") {
        event.preventDefault();
        const edit = $("details.edit", row);
        if (edit) {
          edit.open = true;
          requestAnimationFrame(() => $("input[name=value]", edit)?.focus());
        }
      }
    });
  });
  $$("details.edit, details.accept", root).filter((el) => once(el, "Esc")).forEach((details) => {
    details.addEventListener("keydown", (event) => {
      if (event.key === "Escape") { event.preventDefault(); details.closest("tr")?.focus(); details.open = false; }
    });
  });

  // Phone menu: the navigation stays open when scripts do not run (see the .js rules in app.css).
  const menu = $("[data-menu]", root);
  if (menu && once(menu, "Menu")) {
    const sidebar = menu.closest("[data-sidebar]");
    const setOpen = (open) => {
      sidebar.classList.toggle("is-open", open);
      menu.setAttribute("aria-expanded", String(open));
    };
    menu.addEventListener("click", () => setOpen(!sidebar.classList.contains("is-open")));
    sidebar.addEventListener("keydown", (event) => {
      if (event.key === "Escape") { setOpen(false); menu.focus(); }
    });
  }

  // Dropzone: the file input covers it, so dropping works natively; this names the file.
  $$("[data-dropzone]", root).filter((el) => once(el, "Drop")).forEach((zone) => {
    const input = $("input[type=file]", zone);
    const name = $("[data-file-name]", zone);
    input.addEventListener("change", () => {
      const file = input.files[0];
      if (file) name.textContent = `${file.name} (${Math.max(1, Math.round(file.size / 1024))} ${name.dataset.kb})`;
    });
    input.addEventListener("dragenter", () => zone.classList.add("is-over"));
    ["dragleave", "drop"].forEach((kind) => input.addEventListener(kind, () => zone.classList.remove("is-over")));
  });

  // Copy the notice text; print the evidence file.
  $$("[data-copy]", root).filter((el) => once(el, "Copy")).forEach((button) => {
    button.addEventListener("click", async () => {
      const source = document.getElementById(button.dataset.copy);
      if (!source) return;
      // Inputs and edited textareas hold their text in value, not in textContent.
      await navigator.clipboard.writeText(source.value ?? source.textContent);
      toast($(".toast")?.dataset.copied || "");
    });
  });
  $$("[data-print]", root).filter((el) => once(el, "Print")).forEach((button) => button.addEventListener("click", () => window.print()));
}

document.addEventListener("DOMContentLoaded", () => setup());
document.addEventListener("htmx:afterSettle", () => setup());
