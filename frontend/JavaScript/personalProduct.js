import { createProductElement,addToLocalStorage, showToast } from "./functions.js"
const template = document.createElement("main")
template.classList.add("main__personal-product")
template.innerHTML = `<a class="back">&larr; Вернутся назад</a>
<div class="persontal-product__content">
          <img src="" />
          <div class="info">
            <p class="info__category"></p>
            <p class="info__name"></p>
            <p class="info__price"></p>
            <p class="info__description"></p>
            <button>Добавить в корзину</button>
          </div>
        </div>`
const insertPlace = document.querySelector(".container-personal-product")
const selectors = {
    name: ".info__name",
    price: ".info__price",
    photo: "img",
    category: ".info__category",
    description: ".info__description"
                }
fetch("xml/products.xml")
    .then(response => response.text())
    .then(
        result => {
            const domParser = new DOMParser()
            const xmlDoc = domParser.parseFromString(result, "text/xml")
            const currentURL = new URLSearchParams(window.location.search);
            const productId = currentURL.get('id');
            const product = xmlDoc.querySelector(`product[id="${productId}"]`);
            const catList = xmlDoc.querySelectorAll("category")
            const el = createProductElement(product,template,selectors,catList)

            const buttonAddToBasket = el.querySelector("button")
            buttonAddToBasket.addEventListener("click", ()=> {
                addToLocalStorage(productId)
                showToast("Товар добавлен в корзину!")
            })
            el.querySelector(".back").addEventListener("click", ()=>{
                window.history.back()
            })
            
            insertPlace.append(el)
            
        })