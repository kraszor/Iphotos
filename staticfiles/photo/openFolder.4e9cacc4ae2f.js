function openFolder() {
    document.getElementById('folder').style.display = 'none';
    let elements = document.getElementsByClassName('groupDetailBox');
    for (let i=0;i<elements.length;i++) {
        elements[i].style.display = 'block';
        setTimeout(function () {
            elements[i].classList.add('detailBoxVisible')
        }, 2)
    }
}