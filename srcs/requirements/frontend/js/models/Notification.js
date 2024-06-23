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
                <strong class="me-auto">PONG</strong>
                <small>now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body" id="winner_txt"></div>
        </div>
        `;
    }

    makeAlert(winner) {
        this.init();
        this.$winnerText = this.$toastContainer.querySelector("#winner_text");

        let temp_txt = "Winner :";
        for(let i = 0; i < winner.length; i++) {
            temp_txt += " ";
            temp_txt += winner[i];
        }

        this.$winnerText = temp_txt;
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