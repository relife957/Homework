/* global $ */
class Main {
    constructor() {
        this.canvas = document.getElementById('main');
        this.input = document.getElementById('input');
        this.canvas.width  = 449; // 16 * 28 + 1
        this.canvas.height = 449; // 16 * 28 + 1
        this.ctx = this.canvas.getContext('2d');
        // this.canvas.addEventListener('mousedown', this.onMouseDown.bind(this));
        // this.canvas.addEventListener('mouseup',   this.onMouseUp.bind(this));
        // this.canvas.addEventListener('mousemove', this.onMouseMove.bind(this));

        this.canvas.addEventListener('touchstart', this.touchStart.bind(this));
        this.canvas.addEventListener('touchleave',   this.touchLeave.bind(this));
        this.canvas.addEventListener('touchend',   this.touchEnd.bind(this));
        this.canvas.addEventListener('touchcancle',   this.touchCancle.bind(this));
        this.canvas.addEventListener('touchmove',   this.touchMove.bind(this));

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
            this.ctx.moveTo((i + 1) * 16,   0);
            this.ctx.lineTo((i + 1) * 16, 449);
            this.ctx.closePath();
            this.ctx.stroke();

            this.ctx.beginPath();
            this.ctx.moveTo(  0, (i + 1) * 16);
            this.ctx.lineTo(449, (i + 1) * 16);
            this.ctx.closePath();
            this.ctx.stroke();
        }
        this.drawInput();
        // $('#output td').text('').removeClass('success');
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

     touchStart(e){
        e.preventDefault();
        if(this.drawing){
            return;
        }
        // this.canvas.style.cursor = 'default';
        this.drawing = true;
        this.prev = this.get1(e.changedTouches[0]);

    };
    touchCancle(e){
        e.preventDefault();
        this.drawing = false;
        this.drawInput();

    };
    touchEnd(e){
        e.preventDefault();
        this.drawing = false;
        this.drawInput();

    };
    touchLeave(e){
        e.preventDefault();
        this.drawing = false;
        this.drawInput();

    };
    touchMove(e){
        e.preventDefault();
        if (this.drawing) {
            var curr = this.get1(e.changedTouches[0]);
            this.ctx.lineWidth = 15;
            this.ctx.lineCap = 'round';
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

    get1(event){
        var rect = this.canvas.getBoundingClientRect();
        return {
            x: event.clientX - rect.left,
            y: event.clientY - rect.top,
        }
    }
    drawInput() {
        var ctx = this.input.getContext('2d');
        var img = new Image();
        img.onload = () => {
            var inputs = [];
            var small = document.createElement('canvas').getContext('2d');
            small.drawImage(img, 0, 0, img.width, img.height, 0, 0, 28, 28);
            var data = small.getImageData(0, 0, 28, 28).data;
            for (var i = 0; i < 28; i++) {
                for (var j = 0; j < 28; j++) {
                    var n = 4 * (i * 28 + j);
                    inputs[i * 28 + j] = (data[n + 0] + data[n + 1] + data[n + 2]) / 3;
                    ctx.fillStyle = 'rgb(' + [data[n + 0], data[n + 1], data[n + 2]].join(',') + ')';
                    ctx.fillRect(j * 5, i * 5, 5, 5);
                }
            }
            if (Math.min(...inputs) === 255) {
                return;
            }
            $.ajax({
                url: '/api/mnist',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(inputs),
                success: (data) => {
                    // for (let i = 0; i < 2; i++) {
                    //     var max = 0;
                    //     var max_index = 0;
                    //     for (let j = 0; j < 10; j++) {
                    //         var value = Math.round(data.results[i][j] * 1000);
                    //         if (value > max) {
                    //             max = value;
                    //             max_index = j;
                    //         }
                    //         var digits = String(value).length;
                    //         for (var k = 0; k < 3 - digits; k++) {
                    //             value = '0' + value;
                    //         }
                    //         var text = '0.' + value;
                    //         if (value > 999) {
                    //             text = '1.000';
                    //         }
                    //         $('#output tr').eq(j + 1).find('td').eq(i).text(text);
                    //     }
                    //     for (let j = 0; j < 10; j++) {
                    //         if (j === max_index) {
                    //             $('#output tr').eq(j + 1).find('td').eq(i).addClass('success');
                    //         } else {
                    //             $('#output tr').eq(j + 1).find('td').eq(i).removeClass('success');
                    //         }
                    //     }
                    // }
                    console.log("successful!!!")
                }
            });
        };
        img.src = this.canvas.toDataURL();
    }
}

$(() => {
    var main = new Main();
    $('#clear').click(() => {
        main.initialize();
    });
});