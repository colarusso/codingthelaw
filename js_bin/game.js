
function load_scratch(project) {
  if (screen.width > 640) {
    if ($('#arcade').is(":hidden")) {
      $('#arcade').show();
      if (project=='416659519'){
        $('#screen').html('<iframe style="margin-top:-5px; margin-left:-4px;" allowtransparency="false" width="658" height="552" bgcolor=#220000 src="https://scratch.mit.edu/projects/embed/'+project+'/" allowfullscreen></iframe> Test test here ');
      } else {
        $('#screen').html('<iframe style="margin-top:-52px; margin-left:-11px;" allowtransparency="false" width="658" height="552" bgcolor=#220000 src="https://scratch.mit.edu/projects/embed/'+project+'/" allowfullscreen></iframe> Test test here ');
      }
    } else {
      $('#screen').html('');
      $('#arcade').hide();
    }
  } else {
    alert('You need to be on a computer with a keyboard to play this game.')
  }
  return true;
}


var myGamePiece;

function startGame() {
    myGamePiece = new component(72, 52, "images/cloud.png", ($( document ).width()/2)+290, 60, "image");
    myGameArea.start();
    $('#title_frame').hide();
}

var myGameArea = {
    canvas : document.createElement("canvas"),
    start : function() {
        this.canvas.width =  $( document ).width();
        this.canvas.height = 290;
        this.context = this.canvas.getContext("2d");
        document.body.insertBefore(this.canvas, document.body.childNodes[0]);
        this.frameNo = 0;
        this.interval = setInterval(updateGameArea, 20);
        },
    clear : function() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    },
    stop : function() {
        clearInterval(this.interval);
    }
}

function component(width, height, color, x, y, type) {
    this.type = type;
    if (type == "image") {
        this.image = new Image();
        this.image.src = color;
    }
    this.width = width;
    this.height = height;
    this.speedX = 0;
    this.speedY = 0;
    this.x = x;
    this.y = y;
    this.update = function() {
        ctx = myGameArea.context;
        if (type == "image") {
            ctx.drawImage(this.image,
                this.x,
                this.y,
                this.width, this.height);
        } else {
            ctx.fillStyle = color;
            ctx.fillRect(this.x, this.y, this.width, this.height);
        }
    }
    this.newPos = function() {
        this.x += this.speedX;
        this.y += this.speedY;
    }
}

function updateGameArea() {
    myGameArea.clear();
    myGamePiece.newPos();
    myGamePiece.update();
}

function moveup() {
    myGamePiece.speedY = -1;
}

function movedown() {
    myGamePiece.speedY = 1;
}

function moveleft() {
    myGamePiece.speedX = -1;
}

function moveright() {
    myGamePiece.speedX = 1;
}

function clearmove() {
    myGamePiece.speedX = 0;
    myGamePiece.speedY = 0;
}
