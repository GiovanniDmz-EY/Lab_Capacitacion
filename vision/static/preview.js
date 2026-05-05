const imageUrl = document.getElementById("imageUrl");
const imageFile = document.getElementById("imageFile");
const imagePreview = document.getElementById("imagePreview");
const previewEmpty = document.getElementById("previewEmpty");
const previewMeta = document.getElementById("previewMeta");
const persistedImage = document.getElementById("persistedImage");

function setPreview(src, message) {
  imagePreview.src = src;
  imagePreview.hidden = false;
  previewEmpty.hidden = true;
  previewMeta.textContent = message;
}

function clearPreview(message) {
  imagePreview.removeAttribute("src");
  imagePreview.hidden = true;
  previewEmpty.hidden = false;
  previewMeta.textContent = message;
}

function previewFromUrl() {
  const url = imageUrl.value.trim();

  if (!url) {
    if (persistedImage.value) {
      setPreview(persistedImage.value, "Previsualizacion del archivo seleccionado.");
      return;
    }

    clearPreview("Carga un archivo o pega una URL para verla antes de analizar.");
    return;
  }

  if (imageFile.value) {
    imageFile.value = "";
  }

  persistedImage.value = "";
  setPreview(url, "Previsualizacion desde URL.");
}

function previewFromFile() {
  const file = imageFile.files && imageFile.files[0];

  if (!file) {
    if (persistedImage.value) {
      setPreview(persistedImage.value, "Previsualizacion del archivo seleccionado.");
      return;
    }

    clearPreview("Carga un archivo o pega una URL para verla antes de analizar.");
    return;
  }

  if (!file.type.startsWith("image/")) {
    clearPreview("El archivo seleccionado no parece ser una imagen.");
    return;
  }

  imageUrl.value = "";
  const reader = new FileReader();
  reader.onload = () => {
    persistedImage.value = reader.result;
    setPreview(reader.result, `${file.name} (${Math.round(file.size / 1024)} KB)`);
  };
  reader.readAsDataURL(file);
}

imagePreview.addEventListener("error", () => {
  clearPreview("No se pudo cargar la previsualizacion. Revisa que la URL sea publica y apunte a una imagen.");
});

imageUrl.addEventListener("input", previewFromUrl);
imageUrl.addEventListener("blur", previewFromUrl);
imageFile.addEventListener("change", previewFromFile);

clearPreview("Carga un archivo o pega una URL para verla antes de analizar.");
if (imageUrl.value.trim()) {
  previewFromUrl();
} else if (persistedImage.value) {
  setPreview(persistedImage.value, "Previsualizacion del archivo seleccionado.");
}
