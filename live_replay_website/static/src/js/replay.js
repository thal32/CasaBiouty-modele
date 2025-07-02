
document.querySelectorAll('select.form-select').forEach(select => {
    select.addEventListener('change', function () {
        const url = this.options[this.selectedIndex].getAttribute('data-url');
        console.log("Option sélectionnée, url =", url);
        if (url) {
            window.location.href = url;
        }
    });
});
