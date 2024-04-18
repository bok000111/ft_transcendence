import {PAGE_MASK, changePage} from "./page.js";

function login(event)
{
    event.preventDefault();
    changePage(PAGE_MASK.MAIN);
}

function logout()
{
    changePage(PAGE_MASK.LOGIN);
}

const loginForm = document.querySelector(".login form");
const logoutBtn = document.querySelector(".header button:nth-child(2)")

loginForm.addEventListener("submit", login);
logoutBtn.addEventListener("click", logout);
