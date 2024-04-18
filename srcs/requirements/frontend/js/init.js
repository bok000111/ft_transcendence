export const DIV = {
    LOGIN: 0x1,
    HEADER: 0x2,
    MAIN: 0x4,
    PONG: 0x8
};

export const divCnt = Object.keys(DIV).length;

export function initDiv(div)
{
    switch (div) {
    case DIV.LOGIN:
        break;
    case DIV.HEADER:
        break;
    case DIV.MAIN:
        break;
    case DIV.PONG:
        break;
    }
}

export function finiDiv(div)
{
    switch (div) {
    case DIV.LOGIN:
        break;
    case DIV.HEADER:
        break;
    case DIV.MAIN:
        break;
    case DIV.PONG:
        break;
    }
}
