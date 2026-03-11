/* ═══════════════════════════════════════════
   DataAnalyzer  –  script.js
   API base URL – change this to your backend
   ═══════════════════════════════════════════ */
const API_BASE = 'http://localhost:5000';  // ← update as needed

/* ── API Route constants ── */
const ROUTES = {
  summary:       `${API_BASE}/api/summary`,
  missingValues: `${API_BASE}/api/missing-values`,
  duplicates:    `${API_BASE}/api/duplicates`,
  outliers:      `${API_BASE}/api/outliers`,
};

/* ══════════════════════════
   1.  NAVBAR – scroll effect
   ══════════════════════════ */
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 20);
});

/* ══════════════════════════
   2.  HAMBURGER
   ══════════════════════════ */
const hamburger   = document.getElementById('hamburger');
const mobileMenu  = document.getElementById('mobileMenu');
hamburger.addEventListener('click', () => {
  mobileMenu.classList.toggle('open');
});

/* ══════════════════════════
   3.  FILE INPUT
   ══════════════════════════ */
const fileInput   = document.getElementById('fileInput');
const fileNameEl  = document.getElementById('fileName');
const uploadZone  = document.getElementById('uploadZone');
let   selectedFile = null;

fileInput.addEventListener('change', () => {
  if (fileInput.files.length) {
    selectedFile = fileInput.files[0];
    fileNameEl.textContent = selectedFile.name;
    fileNameEl.classList.add('chosen');
  }
});

/* Drag & Drop */
uploadZone.addEventListener('dragover', e => {
  e.preventDefault();
  uploadZone.classList.add('dragover');
});
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
uploadZone.addEventListener('drop', e => {
  e.preventDefault();
  uploadZone.classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file && isValidFile(file)) {
    selectedFile = file;
    fileNameEl.textContent = file.name;
    fileNameEl.classList.add('chosen');
  } else {
    showToast('Please drop a CSV or Excel file.', 'error');
  }
});

function isValidFile(file) {
  return /\.(csv|xlsx|xls)$/i.test(file.name);
}

/* ══════════════════════════
   4.  ANALYZE BUTTON  →  navigate to results.html
   ══════════════════════════ */
document.getElementById('analyzeBtn').addEventListener('click', goAnalyze);

function goAnalyze() {
  if (!selectedFile) {
    showToast('Please choose a file first.', 'error');
    return;
  }
  if (!isValidFile(selectedFile)) {
    showToast('Only CSV or Excel files are supported.', 'error');
    return;
  }

  /* Store file in sessionStorage as base64 so results.html can read it */
  const reader = new FileReader();
  reader.onload = () => {
    try {
      sessionStorage.setItem('da_file',     reader.result);
      sessionStorage.setItem('da_filename', selectedFile.name);
      window.location.href = 'results.html';
    } catch (e) {
      /* sessionStorage quota exceeded (very large file) – warn user */
      showToast('File too large to transfer. Try a smaller dataset.', 'error');
    }
  };
  reader.readAsDataURL(selectedFile);
}

/* ══════════════════════════
   7.  SCROLL REVEAL
   ══════════════════════════ */
const revealEls = document.querySelectorAll('.reveal, .reveal-delay-1, .reveal-delay-2');
const observer  = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('revealed');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });
revealEls.forEach(el => observer.observe(el));

/* ══════════════════════════
   8.  TOAST NOTIFICATIONS
   ══════════════════════════ */
function showToast(msg, type = 'info') {
  const toast = document.createElement('div');
  const bg = type === 'error' ? '#dc2626' : '#2563eb';
  Object.assign(toast.style, {
    position: 'fixed', bottom: '1.5rem', left: '50%', transform: 'translateX(-50%)',
    background: bg, color: '#fff', padding: '.7rem 1.4rem',
    borderRadius: '8px', fontSize: '.875rem', fontWeight: '600',
    zIndex: '999', boxShadow: '0 4px 16px rgba(0,0,0,.2)',
    animation: 'slideUp .3s ease',
  });
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}