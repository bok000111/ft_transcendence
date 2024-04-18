import { startGame } from "./pongClass";

const canvasInfo = {
    width: 500,
    height: 500
};

const paddleInfo = {
    width: 70,
    height: 10,
    space: 10,
    speed: 10
};

const ballInfo = {
    radius: 5,
    diffX: 5,
    diffY: 5
};

startGame(4);
