import { DIV, divCnt, initDiv, finiDiv } from "./init.js";

export const PAGE = {
    LOGIN: DIV.LOGIN,
    MAIN: DIV.HEADER | DIV.MAIN,
    PONG: DIV.HEADER | DIV.PONG
};

export class Page
{
    _bitmap;

    constructor(bitmap)
    {
        this._bitmap = bitmap;
    }

    switch(nextPage)
    {
        const diff = this._bitmap ^ nextPage._bitmap;
        let mask = 1;

        for (let i = 0; i < divCnt; ++i, mask <<= 1) {
            if (diff & mask) {
                if (this._bitmap & mask) {
                    finiDiv(mask);
                }
                else {
                    initDiv(mask);
                }
            }
        }
        this._bitmap = nextPage._bitmap;
    }
};
