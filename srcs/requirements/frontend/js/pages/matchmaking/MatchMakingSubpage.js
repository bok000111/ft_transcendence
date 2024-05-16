import Subpage from "../SubPage.js";

class MatchMakingSubpage extends SubPage {
    init() {
        this.$elem.innerHTML = `
            <button id="one">solo</button>
            <button id="two">2 players</button>
            <button id="three">3 players</button>
            <button id="four">4 players</button>
        `;

        
    }
}