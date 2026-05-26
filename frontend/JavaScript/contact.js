import {showToast } from "./functions.js"

const form = document.getElementById("cont-form")

form.addEventListener("submit", (e) => {
    e.preventDefault()
    form.reset()
    showToast("Ваше сообщение отправлено. Мы свяжемся с вами.", 3000)
})