export function getCat(id, categoryList) {
    for (const category of categoryList)
        if (category.getAttribute("id") === id) {
                return category.textContent
        }
}

export function getID(name, categoryList) { 
    for (const category of categoryList) {
        if(name.toLowerCase() === category.textContent.toLowerCase()) {
            return category.getAttribute("id")
        }
    }
    return "all"
}

export function createProductElement(product, template, selectors, catList) {
    let newEl = template.cloneNode(true)
    const name = product.querySelector("name").textContent;
    const price = product.querySelector("price").textContent;
    const photo = product.querySelector("photo").textContent;
    const categoryId = product.querySelector("categoryId").textContent;
    newEl.querySelector(selectors.name).textContent = name
    newEl.querySelector(selectors.price).textContent = price
    newEl.querySelector(selectors.photo).src = photo
    newEl.querySelector(selectors.category).textContent = getCat(categoryId,catList)
    newEl.dataset.id = product.getAttribute("id")
    if (selectors.description) {
        const desc = product.querySelector("description").textContent
        newEl.querySelector(selectors.description).textContent = desc
    }
    return newEl
}

export function addToLocalStorage(id) {
    let allID = localStorage.getItem("ids") || ""
    let ids = allID ? allID.split(",") : []
    ids.push(id)
    localStorage.setItem("ids", ids.join(","))
    
}

export function getFromLocalStorage() {
    let allID = localStorage.getItem("ids") || ""
    return allID ? allID.split(",") : []
}

export function deleteFromLocalStorage(id) { 
    let ids = getFromLocalStorage()
    const index = ids.indexOf(id)
     if (index !== -1) {
        ids.splice(index, 1) 
    }
    localStorage.setItem("ids", ids.join(","))
}

export function showToast(message, duration = 3000) {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = 'toast'; 
    toast.innerHTML = `
        <span class="toast__text">${message}</span>
    `;
    container.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('toast--hiding');
        toast.addEventListener('animationend', () => toast.remove(), { once: true });
    }, duration);
}