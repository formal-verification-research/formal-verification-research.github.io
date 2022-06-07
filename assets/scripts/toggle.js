function toggle(name) {
  var tex = document.getElementById('c' + name);
  var but = document.getElementById('l' + name);
  var tog = document.getElementById('t' + name);
  if (tex.style.display === "none") {
    tex.style.display = "block";
    but.style.display = "inline";
    tog.innerHTML = 'Close BibTex&nbsp;<i class="fa-solid fa-circle-xmark"></i>'
  } else {
    tex.style.display = "none";
    but.style.display = "none";
    tog.innerHTML = 'BibTeX&nbsp;<i class="far fa-file-alt"></i>'
  }
}

function copyBibtex(name) {
  const copyText = document.getElementById('c' + name).textContent;
  const textArea = document.createElement('textarea');
  textArea.textContent = copyText;
  document.body.append(textArea);
  textArea.select();
  document.execCommand("copy");
  var but = document.getElementById('l' + name);
  but.innerHTML = 'BibTeX Copied&nbsp;<i class="fas fa-check"></i>';
  but.style.background = "#088fa3";
  setTimeout( function() {
    but.innerHTML = 'Copy BibTeX&nbsp;<i class="far fa-copy"></i>';
    but.style.background = "#baebf3";},
    1000);
}