/* Cierra el desplegable del menú al tocar fuera o al pulsar Escape. */
(function () {
  var abiertos = function () {
    return document.querySelectorAll("nav details.desplegable[open]");
  };
  document.addEventListener("click", function (e) {
    Array.prototype.forEach.call(abiertos(), function (d) {
      if (!d.contains(e.target)) d.removeAttribute("open");
    });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    Array.prototype.forEach.call(abiertos(), function (d) {
      d.removeAttribute("open");
      var s = d.querySelector("summary");
      if (s) s.focus();
    });
  });
})();
