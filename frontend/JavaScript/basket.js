import { getFromLocalStorage, createProductElement,deleteFromLocalStorage, showToast } from "./functions.js"
const template = document.createElement("li")
template.innerHTML = `<article class="product-template product-template__basket">
              <img src="" class="product-img" />
              <div class="product__info">
                <p class="product-name"></p>
                <p class="cat"></p>
              </div>
              <p class="product-price"></p>
              <button class="product-remove">
                <img src="photos/svg/мусорка.svg" />
              </button>
            </article>`

const insertPlace = document.querySelector(".basket-list")  
const totalPriceHtml = document.querySelector(".total-price")
const totalPoductHtml = document.querySelector(".total-product")

  
const selectors = {
    name: ".product-name",
    price: ".product-price", 
    photo: ".product-img",   
    category: ".cat"
    }


function getInfo(xmlDoc) {
    let ids = getFromLocalStorage()
    console.log(ids)
    let totalProduct = ids.length
    let totalPrice = 0
    
    ids.forEach(productId => {
        const product = xmlDoc.querySelector(`product[id="${productId}"]`)
        const price = product.querySelector("price").textContent
        totalPrice += Number(price)
    });
    totalPriceHtml.textContent = "Общая сумма: " + totalPrice + " BYN"
    totalPoductHtml.textContent = "Количество товаров: " + totalProduct
}
function showBascket(xmlDoc, catList) {
    let idsArray = getFromLocalStorage()
    for (let productId of idsArray) {
        const product = xmlDoc.querySelector(`product[id="${productId}"]`);
        let newEl = createProductElement(product,template,selectors,catList)
        insertPlace.append(newEl)
    }
} 

function checkEmptyBasket() {
    const emptyMsg = document.getElementById("basket-empty")
    const isEmpty = insertPlace.children.length === 0
    const order_inf = document.querySelector(".order-info")
    emptyMsg.style.display = isEmpty ? "block" : "none"
    order_inf.style.display = isEmpty ? "none" : "flex"
}

fetch("xml/products.xml")
    .then(response => response.text())
    .then(
        result => 
        {
            const domParser = new DOMParser()
            const xmlDoc = domParser.parseFromString(result, "text/xml")
            const categoryList = xmlDoc.querySelectorAll("category")
            showBascket(xmlDoc, categoryList)
            getInfo(xmlDoc)
            checkEmptyBasket()
            window.addEventListener("storage" ,()=>{
                showBascket(xmlDoc,categoryList)
                getInfo(xmlDoc)
                 checkEmptyBasket()
            })
            insertPlace.addEventListener("click" , event => {
            const target = event.target.closest(".product-remove")
            if (target) {
                let deletedId = event.target.closest("li").dataset.id
                deleteFromLocalStorage(deletedId)
                event.target.closest("li").remove()
                getInfo(xmlDoc)
                checkEmptyBasket()
                return
            }
            const li = event.target.closest("li")
            if (li) {
            const id = li.dataset.id
            window.location.href = `productPage.html?id=${id}`
        }

        })   
            

        }
    )


const orderMenuBackground = document.querySelector(".basket-form");
const makeOrderBtn = document.querySelector("#make-order");

makeOrderBtn.addEventListener("click", () => {
    orderMenuBackground.style.display = "block"; 
});

document.querySelector("#chanel").addEventListener("click", () =>{
    orderMenuBackground.style.display = "none"; 
})


const form = document.querySelector(".deliviry-form")
form.addEventListener("submit", (e) => {
    e.preventDefault()
    orderMenuBackground.style.display = "none"
    form.reset()

    localStorage.removeItem("ids")
    document.querySelector(".basket-list").innerHTML = ""
    document.querySelector(".total-price").textContent = "Общая сумма: 0 BYN"
    document.querySelector(".total-product").textContent = "Количество товаров: 0"
    checkEmptyBasket()
    showToast("Ваш заказ принят! Мы свяжемся с вами в ближайшее время.", 5000)
})
