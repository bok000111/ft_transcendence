class ToastNot {
    $toastContainer;
    $winnerText;
    toastEl;
    toast;

    constructor() {
        this.init();
    }

    init() {
        this.$toastContainer = document.querySelector("#toast-container");

        this.$toastContainer.innerHTML = `
        <div class="toast" id="winner_toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <img src="" class="rounded me-2" alt="">
                <strong class="me-auto">Pong</strong>
                <small>now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body" id="winner_txt"></div>
        </div>
        `;
    }

    makeAlert(winner) {
        this.init();
        this.$winnerText = this.$toastContainer.querySelector("#winner_txt");

        let temp_txt = document.createElement("div");

        temp_txt.innerHTML = `Winner :`;

        for(let i = 0; i < winner.length; i++) {
            temp_txt.innerHTML += ` `;
            temp_txt.innerHTML += `${winner[i]}`;
            if (i + 1 !== winner.length) {
                temp_txt.innerHTML += `,`;
            }
        }

        this.$winnerText.appendChild(temp_txt);
        this.toastEl = this.$toastContainer.querySelector("#winner_toast");
        this.toast = new bootstrap.Toast(this.toastEl, {
            animation: true,
            autohide: true,
            delay: 3000
        });

        this.toast.show();
    }
}

export const toastNot = new ToastNot();
