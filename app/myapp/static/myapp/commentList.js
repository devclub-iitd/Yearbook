var search = document.querySelector('.input100');
var results = document.querySelector('#searchresults');
var templateContent = document.querySelector('#students').content;
search.addEventListener('keyup', function handler(event) {
    while (results.children.length) results.removeChild(results.firstChild);
    var inputVal = new RegExp(search.value.trim(), 'i');
    var set = Array.prototype.reduce.call(templateContent.cloneNode(true).children, function searchFilter(frag, item, i) {
        if (inputVal.test(item.textContent) && frag.children.length < 6) {
					frag.appendChild(item);
					}
        return frag;
    }, document.createDocumentFragment());
    results.appendChild(set);
});
