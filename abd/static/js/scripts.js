document.addEventListener("DOMContentLoaded", () => {
    const toggleToImage = document.getElementById("toggle-to-image");
    const toggleToText = document.getElementById("toggle-to-text");
    const imageSearch = document.getElementById("image-search");
    const textSearch = document.getElementById("text-search");

    // التبديل بين البحث بالصورة والنص
    toggleToImage.addEventListener("click", () => {
        // إظهار البحث بالصورة
        imageSearch.classList.add("active");
        textSearch.classList.remove("active");

        // تفعيل التبويب
        toggleToImage.classList.add("active-tab");
        toggleToText.classList.remove("active-tab");
    });

    toggleToText.addEventListener("click", () => {
        // إظهار البحث بالنص
        textSearch.classList.add("active");
        imageSearch.classList.remove("active");

        // تفعيل التبويب
        toggleToText.classList.add("active-tab");
        toggleToImage.classList.remove("active-tab");
    });

    // التبديل الافتراضي للبحث بالصورة
    imageSearch.classList.add("active");
    textSearch.classList.remove("active");
});