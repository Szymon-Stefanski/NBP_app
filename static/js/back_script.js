function back() {
    document.getElementById("backButton").addEventListener("click", function () {
        var url = this.getAttribute("data-href-template");
        window.location.href = url;
    });
}
