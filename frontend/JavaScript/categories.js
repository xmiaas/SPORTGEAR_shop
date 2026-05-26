import { getCat, createProductElement, getID } from "./functions.js"
//Боковоая панель с категориями 
const liTagTemplate = document.createElement("li")
const cartProductTemplate = document.createElement("article")
cartProductTemplate.classList.add("product-cart")
cartProductTemplate.innerHTML = `
    <div class="product-cart__img">
        <img src="" />
    </div>
    <div class="product-cart__info">
        <p class="product-category"></p>
        <p class="product-name"></p>
        <p class="product-price"></p>
    </div>`         
const selectors = {
                    name: ".product-name",
                    price: ".product-price",
                    photo: "img",
                    category: ".product-category"
                }


const categoryListHtml = document.querySelector(".cat_list")
const productConteiner = document.querySelector(".product-container")


const displayProduct = (productList, categoryList, currentID="all") => {
    productConteiner.innerHTML = ""

    for (let product of productList) { 
        if (currentID === "all" || currentID === product.querySelector("categoryId").textContent) {
            let newEl = createProductElement(product,cartProductTemplate,selectors,categoryList)
              productConteiner.append(newEl)
        }
                    
}
}
const url = new URL(window.location.href)
fetch("xml/products.xml")
    .then(response => response.text())
    .then(
        result => 
        {
            const domParser = new DOMParser()
            const xmlDoc = domParser.parseFromString(result, "text/xml")
            const categoryList = xmlDoc.querySelectorAll("category")

            

            //бок меню
            for (const cat of categoryList) {
                const liTagClone = liTagTemplate.cloneNode()
                liTagClone.dataset.id = cat.getAttribute("id")
                liTagClone.textContent = cat.textContent
                categoryListHtml.append(liTagClone)
                
            }   

            //карточки
            const cart = cartProductTemplate.querySelector(".product-cart")
            const productList = xmlDoc.querySelectorAll("product")
            displayProduct(productList, categoryList)

            function clickOnLi(targetLi, isInit=false) {
                if (!targetLi) return;
                const currentActive = categoryListHtml.querySelector(".li-active");

                if (currentActive && currentActive !== targetLi) {
                    currentActive.classList.remove("li-active");
                }

                targetLi.classList.add("li-active");
                            
            
                let currentID = getID(targetLi.textContent, categoryList)
                displayProduct(productList,categoryList, currentID)
                if (!isInit) {
                    url.searchParams.set("id", currentID)
                    window.history.pushState({}, "", url)
                }
            }
            const params = new URLSearchParams(window.location.search);
            const categoryID = params.get('id');

            if (categoryID) {
                const targetLi = categoryListHtml.querySelector(`li[data-id="${categoryID}"]`);
                if (targetLi) {
                    clickOnLi(targetLi,true); 
                }
            } else {
                displayProduct(productList, categoryList, "all");
            }
            //!!!!!!
            categoryListHtml.addEventListener("click", (event) => {
                //смена цвета при нажатии
                const targetLi = event.target.closest("li");
                clickOnLi(targetLi)
                        

        });
         //!!!!!!
        
            
        }
    )
    

    



productConteiner.addEventListener("mouseover", (event) => {
    const card = event.target.closest(".product-cart")
    card.querySelector("img").classList.add("img-active")
    })

productConteiner.addEventListener("mouseout", (event) => {
    const card = event.target.closest(".product-cart")
    card.querySelector("img").classList.remove("img-active")
})

productConteiner.addEventListener("click", (event) =>{
    const cart = event.target.closest(".product-cart")
    const id = cart.dataset.id
    window.location.href=`productPage.html?id=${id}`
})