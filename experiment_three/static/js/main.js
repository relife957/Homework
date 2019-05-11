/* global $ */
class Main {
    constructor() {
        this.canvas = document.getElementById('main');
        this.canvas.width = 449; // 16 * 28 + 1
        this.canvas.height = 449; // 16 * 28 + 1
        this.ctx = this.canvas.getContext('2d');
        this.canvas.addEventListener('mousedown', this.onMouseDown.bind(this));
        this.canvas.addEventListener('mouseup', this.onMouseUp.bind(this));
        this.canvas.addEventListener('mousemove', this.onMouseMove.bind(this));

        this.canvas.addEventListener('touchstart', this.touchStart.bind(this));
        this.canvas.addEventListener('touchleave', this.touchLeave.bind(this));
        this.canvas.addEventListener('touchend', this.touchEnd.bind(this));
        this.canvas.addEventListener('touchcancle', this.touchCancle.bind(this));
        this.canvas.addEventListener('touchmove', this.touchMove.bind(this));

        this.ws = new WebSocket("ws://localhost:8888/ws");
        this.initialize();
    }

    initialize() {
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.fillRect(0, 0, 449, 449);
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(0, 0, 449, 449);
        this.ctx.lineWidth = 0.05;
        for (var i = 0; i < 27; i++) {
            this.ctx.beginPath();
            this.ctx.moveTo((i + 1) * 16, 0);
            this.ctx.lineTo((i + 1) * 16, 449);
            this.ctx.closePath();
            this.ctx.stroke();

            this.ctx.beginPath();
            this.ctx.moveTo(0, (i + 1) * 16);
            this.ctx.lineTo(449, (i + 1) * 16);
            this.ctx.closePath();
            this.ctx.stroke();
        }
        $('#show').text('');
    }

    onMouseDown(e) {

        this.canvas.style.cursor = 'default';
        this.drawing = true;
        this.prev = this.getPosition(e.clientX, e.clientY);
    }

    onMouseUp() {
        this.drawing = false;
        this.drawInput();
    }

    onMouseMove(e) {
        if (this.drawing) {
            var curr = this.getPosition(e.clientX, e.clientY);
            this.ctx.lineWidth = 15;
            this.ctx.lineCap = 'round';
            this.ctx.beginPath();
            this.ctx.moveTo(this.prev.x, this.prev.y);
            this.ctx.lineTo(curr.x, curr.y);
            this.ctx.stroke();
            this.ctx.closePath();
            this.prev = curr;
        }
    }

    touchStart(e) {
        e.preventDefault();
        if (this.drawing) {
            return;
        }
        // this.canvas.style.cursor = 'default';
        this.drawing = true;
        this.prev = this.get1(e.changedTouches[0]);

    };

    touchCancle(e) {
        e.preventDefault();
        this.drawing = false;
        this.drawInput();

    };

    touchEnd(e) {
        e.preventDefault();
        this.drawing = false;
        this.drawInput();

    };

    touchLeave(e) {
        e.preventDefault();
        this.drawing = false;
        this.drawInput();

    };

    touchMove(e) {
        e.preventDefault();
        if (this.drawing) {
            var curr = this.get1(e.changedTouches[0]);
            this.ctx.lineWidth = 15;
            this.ctx.lineCap = 'round';
            this.ctx.lineJoin = 'round';
            this.ctx.beginPath();
            this.ctx.moveTo(this.prev.x, this.prev.y);
            this.ctx.lineTo(curr.x, curr.y);
            this.ctx.stroke();
            this.ctx.closePath();
            this.prev = curr;
        }
    };

    getPosition(clientX, clientY) {
        var rect = this.canvas.getBoundingClientRect();
        return {
            x: clientX - rect.left,
            y: clientY - rect.top
        };
    }

    get1(event) {
        var rect = this.canvas.getBoundingClientRect();
        return {
            x: event.clientX - rect.left,
            y: event.clientY - rect.top,
        }
    }

    drawInput() {
        var img = new Image();
        img.src = this.canvas.toDataURL();
        img.onload = () => {
            var inputs = [];
            var small = document.createElement('canvas').getContext('2d');
            small.drawImage(img, 0, 0, img.width, img.height, 0, 0, 28, 28);
            var data = small.getImageData(0, 0, 28, 28).data;
            for (var i = 0; i < 28; i++) {
                for (var j = 0; j < 28; j++) {
                    var n = 4 * (i * 28 + j);
                    inputs[i * 28 + j] = (data[n] + data[n + 1] + data[n + 2]) / 3;
                }
            }
            if (Math.min(...inputs) === 255) {
                return;
            }

            this.ws.send(JSON.stringify(inputs));

            this.ws.onmessage = function (event) {
                console.log("111111111");
                $("#show").text("预测结果如下: " + event.data);
            }
        };
    }
}

$(() => {
    var main = new Main();
    $('#clear').click(() => {
        main.initialize();
    });
});


