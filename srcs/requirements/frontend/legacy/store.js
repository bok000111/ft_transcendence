import { observe, observer } from "./core/Observer.js";
import { Store } from "./core/Store.js";

const store = new Store({
    state: new observer({
        a: 10,
        b: 20
    }),
    mutations: {
        SET_A(state, payload)
        {
            state.a = payload;
        },
        SET_B(state, payload)
        {
            state.b = payload;
        }
    }
});
observe(() => console.log(`a: ${store.state.a}, b: ${store.state.b}`));

store.commit("SET_A", 100);
store.commit("SET_B", 200);
