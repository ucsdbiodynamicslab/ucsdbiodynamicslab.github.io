fetch('/assets/data/footers.json')
  .then(response => response.json())
  .then(data => {
    const arr = data.footers;
    const pick = arr[Math.floor(Math.random() * arr.length)];
    document.getElementById('rotating-footer').textContent = pick;
  })
  .catch(() => {});