(function () {
  const konami = [
    "arrowup","arrowup",
    "arrowdown","arrowdown",
    "arrowleft","arrowright",
    "arrowleft","arrowright",
    "b","a"
  ];

  let buffer = [];

  window.addEventListener("keydown", function (e) {
    // Normalize key to lowercase
    const key = e.key.toLowerCase();
    console.log("Key pressed:", key);

    buffer.push(key);
    buffer = buffer.slice(-konami.length);

    if (buffer.join(",") === konami.join(",")) {
      console.log("Konami code detected!");
      window.location.href = "/secret/";
    }
  });
})();