export class Store
{
    #state;
    #mutations;
    #actions;
    /**
     * 외부에서 접근할 때에는 #state가 아닌 아래의 state를 통해서 접근한다.
     * 실제로 state 내부에는 어떤 멤버변수도 존재하지 않는다.
     * 아래의 defineProperty를 통해서 #state를 접근하는 중간자 역할을 함.
     * 따라서 외부에서 #state의 조작이 불가능하다.
     */
    state = {};

    constructor({ state, mutations, actions })
    {
        this.#state = state;
        this.#mutations = mutations;
        this.#actions = actions;

        Object.keys(this.#state).forEach(key => {
            Object.defineProperty(
                this.state,
                key,
                {
                    get: () => this.#state[key]
                }
            )
        })
    }

    commit(action, payload)
    {
        // 내부의 state 조작은 commit 함수를 통해서만 가능하다.
        this.#mutations[action](this.#state, payload);
    }

    dispatch(action, payload)
    {
        return this.#actions[action]({
            state: this.#state,
            commit: this.commit.bind(this),
            dispatch: this.dispatch.bind(this)
        }, payload);
    }
};