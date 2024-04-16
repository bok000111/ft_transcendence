const cnvs = document.querySelector(".pong canvas");
let ctx = cnvs.getContext("2d");

const paddleInfo = {
    width: 70,
    height: 10,
    space: 10,
    speed: 10
}

const ballInfo = {
    radius: 5,
    diffX: 5,
    diffY: 5
}

const CONFLICT = {
    NONE: 0x0,
    HORIZONTAL: 0x1,
    VERTICAL: 0x2,
    WALL_PLAYER1: 0x4,
    WALL_PLAYER2: 0x8,
    WALL_PLAYER3: 0x10,
    WALL_PLAYER4: 0x20,
    WALL_PLAYER_MASK: 0x3c
};
Object.freeze(CONFLICT);

class AObject
{
    constructor(posX, posY, diffX, diffY)
    {
        this._posX = posX;
        this._posY = posY;
        this._diffX = diffX;
        this._diffY = diffY;
    }

    get posX()
    {
        return this._posX;
    }

    get posY()
    {
        return this._posY;
    }

    get diffX()
    {
        return this._diffX;
    }

    get diffY()
    {
        return this._diffY;
    }

    move() {}
    draw() {}
};

class Paddle extends AObject
{
    constructor(widthX, widthY, posX, posY, diffX, diffY)
    {
        super(posX, posY, diffX, diffY);
        this._widthX = widthX;
        this._widthY = widthY;
        this._movingLeft = false;
        this._movingRight = false;
    }

    reset(obj)
    {
        this._posX = obj._posX;
        this._posY = obj._posY;
        this._diffX = obj._diffX;
        this._diffY = obj._diffY;
        this._widthX = obj._widthX;
        this._widthY = obj._widthY;
        this._movingLeft = false;
        this._movingRight = false;
    }

    /* it doesn't move if left and right are pressed simultaneously. */
    _moveLeft()
    {
        const afterX = this._posX - this._diffX;
        const afterY = this._posY - this._diffY;

        if (afterX - this._widthX / 2 >= 0 && afterX + this._widthX / 2 <= cnvs.width)
            this._posX = afterX;
        if (afterY - this._widthY / 2 >= 0 && afterY + this._widthY / 2 <= cnvs.height)
            this._posY = afterY;
    }

    _moveRight()
    {
        const afterX = this._posX + this._diffX;
        const afterY = this._posY + this._diffY;

        if (afterX - this._widthX / 2 >= 0 && afterX + this._widthX / 2 <= cnvs.width)
            this._posX = afterX;
        if (afterY - this._widthY / 2 >= 0 && afterY + this._widthY / 2 <= cnvs.height)
            this._posY = afterY;
    }

    inside(posX, posY)
    {
        if (posX > this._posX - this._widthX / 2 && posX < this._posX + this._widthX / 2
            && posY > this._posY - this._widthY / 2 && posY < this._posY + this._widthY / 2) {
            return true;
        }
        else {
            return false;
        }
    }

    move()
    {
        if (!(this._movingLeft ^ this._movingRight))
            return;
        if (this._movingLeft) {
            this._moveLeft();
        }
        else if (this._movingRight) {
            this._moveRight();
        }
    }

    draw()
    {
        ctx.fillRect(this._posX - this._widthX / 2, this._posY - this._widthY / 2, this._widthX, this._widthY);
    }

    get widthX()
    {
        return this._widthX;
    }

    get widthY()
    {
        return this._widthY;
    }

    get movingLeft()
    {
        return this._movingLeft;
    }

    get movingRight()
    {
        return this._movingRight;
    }

    set movingLeft(value)
    {
        this._movingLeft = value;
    }

    set movingRight(value)
    {
        this._movingRight = value;
    }
};

class Ball extends AObject
{
    constructor(posX, posY, diffX, diffY, radius)
    {
        super(posX, posY, diffX, diffY);
        this._radius = radius;
    }
    
    reset(obj)
    {
        this._posX = obj._posX;
        this._posY = obj._posY;
        this._diffX = obj._diffX;
        this._diffY = obj._diffY;
        this._radius = obj._radius;
    }

    /* X방향, Y방향 중 어느쪽에서 충돌했는지 알려주는 함수 */
    _conflict(players)
    {
        const afterX = this._posX + this._diffX;
        const afterY = this._posY + this._diffY;
        let conflictResult = CONFLICT.NONE;

        for (i = 0; i < players.length; ++i) {
            if (players[i].paddle.inside(afterX + this._radius, afterY)
                || players[i].paddle.inside(afterX - this._radius, afterY)) {
                conflictResult |= CONFLICT.HORIZONTAL;
            }
            if (players[i].paddle.inside(afterX, afterY + this._radius)
                || players[i].paddle.inside(afterX, afterY - this._radius)) {
                conflictResult |= CONFLICT.VERTICAL;
            }
        }
        if (afterX + this._radius > cnvs.width) {
            conflictResult |= CONFLICT.WALL_PLAYER1;
            conflictResult |= CONFLICT.HORIZONTAL;
        }
        if (afterX - this._radius < 0) {
            conflictResult |= CONFLICT.WALL_PLAYER2;
            conflictResult |= CONFLICT.HORIZONTAL;
        }
        if (afterY + this._radius > cnvs.width) {
            conflictResult |= CONFLICT.VERTICAL;
            if (players.length >= 3) {
                conflictResult |= CONFLICT.WALL_PLAYER3;
            }
        }
        if (afterY - this._radius < 0) {
            conflictResult |= CONFLICT.VERTICAL;
            if (players.length >= 4) {
                conflictResult |= CONFLICT.WALL_PLAYER4;
            }
        }
        return conflictResult;
    }

    move(players)
    {
        const conflictResult = this._conflict(players);

        if (conflictResult & CONFLICT.WALL_PLAYER_MASK) {
            return conflictResult;
        }
        if (conflictResult & CONFLICT.HORIZONTAL) {
            this._diffX *= -1;
        }
        if (conflictResult & CONFLICT.VERTICAL) {
            this._diffY *= -1;
        }
        this._posX += this._diffX;
        this._posY += this._diffY;
        return conflictResult;
    }

    draw()
    {
        ctx.beginPath();
        ctx.arc(this._posX, this._posY, this._radius, 0, Math.PI * 2, true);
        ctx.fill();
    }

    get radius()
    {
        return this._radius;
    }
};

const initPaddles = [
    new Paddle(paddleInfo.height, paddleInfo.width, paddleInfo.space + paddleInfo.height / 2, cnvs.height / 2, 0, 10),
    new Paddle(paddleInfo.height, paddleInfo.width, cnvs.width - paddleInfo.space - paddleInfo.height / 2, cnvs.height / 2, 0, -10),
    new Paddle(paddleInfo.width, paddleInfo.height, cnvs.width / 2, cnvs.height - paddleInfo.space - paddleInfo.height / 2, 10, 0),
    new Paddle(paddleInfo.width, paddleInfo.height, cnvs.width / 2, paddleInfo.space + paddleInfo.height / 2, -10, 0)
]

const initKeys = [
    { leftKey: "w", rightKey: "s" },
    { leftKey: "ArrowDown", rightKey: "ArrowUp" },
    { leftKey: "c", rightKey: "v" },
    { leftKey: ".", rightKey: "," }
]

const initBalls = [
    new Ball(cnvs.width / 2, cnvs.height / 2, ballInfo.diffX, ballInfo.diffY, ballInfo.radius)
]

class Score
{
    constructor()
    {
        this._tag = document.createElement("h1");
        this._score = 0;
        this._tag.textContent = `${this._score}`;
        document.querySelector(".scoreboard").appendChild(this._tag);
    }

    incScore()
    {
        ++this._score;
        this._tag.textContent = `${this._score}`;
    }

    decScore()
    {
        --this._score;
        this._tag.textContent = `${this._score}`;
    }

    get score()
    {
        return this._score;
    }
};

class Player
{
    constructor(paddle, leftKey, rightKey)
    {
        this._paddle = new Paddle(paddle.widthX, paddle.widthY, paddle.posX, paddle.posY, paddle.diffX, paddle.diffY);
        this._keydownHandler = this._makeKeyEventHandler(leftKey, rightKey, true);
        this._keyupHandler = this._makeKeyEventHandler(leftKey, rightKey, false);
        this._score = new Score();
        document.addEventListener("keydown", this._keydownHandler);
        document.addEventListener("keyup", this._keyupHandler);
    }

    _makeKeyEventHandler(leftKey, rightKey, value)
    {
        return ((event) => {
            if (event.key === leftKey) {
                this._paddle.movingLeft = value;
            }
            else if (event.key === rightKey) {
                this._paddle.movingRight = value;
            }
        });
    }

    incScore()
    {
        this._score.incScore();
    }

    decScore()
    {
        this._score.decScore();
    }

    getScore()
    {
        return this._score.score;
    }

    move()
    {
        this._paddle.move();
    }

    draw()
    {
        this._paddle.draw();
    }

    get paddle()
    {
        return this._paddle;
    }
};

function scoreCalc(players, moveResult)
{
    players.forEach((elem) =>
    {
        elem.incScore();
    })
    if (moveResult & CONFLICT.WALL_PLAYER1) {
        players[0].decScore();
    }
    if (moveResult & CONFLICT.WALL_PLAYER2) {
        players[1].decScore();
    }
    if (moveResult & CONFLICT.WALL_PLAYER3) {
        players[2].decScore();
    }
    if (moveResult & CONFLICT.WALL_PLAYER4) {
        players[3].decScore();
    }
}

function resetGame(players, balls)
{
    for (i = 0; i < players.length; ++i) {
        players[i].paddle.reset(initPaddles[i]);
    }
    for (i = 0; i < balls.length; ++i) {
        balls[i].reset(initBalls[i]);
    }
}

/* player가 움직인 후 그 다음에 공이 움직여야 공이 끼는 상태를 막을 수 있다. */
function moveAll(players, balls)
{
    players.forEach((instance) => {
        instance.move();
    })
    balls.forEach((instance) => {
        const moveResult = instance.move(players);

        if (moveResult & CONFLICT.WALL_PLAYER_MASK) {
            scoreCalc(players, moveResult);
            resetGame(players, balls);
        }
    })
}

function drawAll(players, balls)
{
    players.forEach((instance) => {
        instance.draw();
    })
    balls.forEach((instance) => {
        instance.draw();
    })
}

function show(players, balls)
{
    ctx.clearRect(0, 0, cnvs.width, cnvs.height);
    moveAll(players, balls);
    drawAll(players, balls);
}

function startGame(playerNum)
{
    const players = [];
    const balls = [];
    balls.push(new Ball(initBalls[0].posX, initBalls[0].posY, initBalls[0].diffX, initBalls[0].diffY, initBalls[0].radius));

    for (i = 0; i < playerNum; ++i) {
        players.push(new Player(initPaddles[i], initKeys[i].leftKey, initKeys[i].rightKey));
    }

    setInterval(show, 50, players, balls);
}

startGame(4);
