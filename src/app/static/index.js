(function() {
	var canvas = document.querySelector("#canvas");
	var context = canvas.getContext("2d");
	canvas.width = 900;
	canvas.height = 300;
	var Mouse = {x:0, y:0};
	var lastMouse = {x:0, y:0};
	var Touch = {x:0, y:0};
	var lastTouch = {x:0, y:0};
	context.fillStyle = "white";
	context.fillRect(0, 0, canvas.width, canvas.height);
	context.color = "black";
	context.lineWidth = 10;
    context.lineJoin = context.lineCap = 'round';
	
	debug();
	
	//ipad 
	canvas.addEventListener("touchmove", function(e) {
		e.preventDefault();
		lastTouch.x=Touch.x;
		lastTouch.y=Touch.y;
		Touch.x=e.changedTouches[0].pageX- this.offsetLeft-15;
		Touch.y=e.changedTouches[0].pageY- this.offsetTop-15;
	
		
	}, );

	canvas.addEventListener("touchstart", function(e) {	
		Touch.x=e.changedTouches[0].pageX- this.offsetLeft-15;
		Touch.y=e.changedTouches[0].pageY- this.offsetTop-15;
		
			
		
		canvas.addEventListener("touchmove",onPaintTouch, false);
		
	}, );
	

	//ordinateur
	canvas.addEventListener("mousemove", function(e) {
		lastMouse.x = Mouse.x;
		lastMouse.y = Mouse.y;

		Mouse.x = e.pageX - this.offsetLeft-15;
		Mouse.y = e.pageY - this.offsetTop-15;
	}, false);

	canvas.addEventListener("mousedown", function(e) {
		canvas.addEventListener("mousemove", onPaint, false);
	}, false);

	document.addEventListener("mouseup", function() {
		canvas.removeEventListener("mousemove", onPaint, false);
	}, false);

	var onPaint = function() {	
		context.lineWidth = context.lineWidth;
		context.lineJoin = "round";
		context.lineCap = "round";
		context.strokeStyle = context.color;
	
		context.beginPath();
		context.moveTo(lastMouse.x, lastMouse.y);
		context.lineTo(Mouse.x,Mouse.y );
		context.closePath();
		context.stroke();
	};

	var onPaintTouch = function() {	
		context.lineWidth = context.lineWidth;
		context.lineJoin = "round";
		context.lineCap = "round";
		context.strokeStyle = context.color;
	
		context.beginPath();
		context.moveTo(lastTouch.x, lastTouch.y);
		context.lineTo(Touch.x,Touch.y );
		context.closePath();
		context.stroke();
	};

	function debug() {
		$("#clearButton").on("click", function() {
			context.clearRect( 0, 0, canvas.width, canvas.height );
			context.fillStyle="white";
			context.fillRect(0,0,canvas.width,canvas.height);
		});
	}

	//Affichage + traitement de l'image importé
	var URL = window.webkitURL || window.URL;
    var input = document.getElementById('file');
    input.addEventListener('change', handleFiles, false);

	function handleFiles(e) {
		var context = document.getElementById('canvas').getContext('2d');
	    var reader  = new FileReader();
	    var file = e.target.files[0];
	    // load to image to get it's width/height
	    var img = new Image();
	    img.onload = function() {
	    	context.canvas.width=900
	    	context.canvas.height=300
	    	
		    if( img.width > context.canvas.width) {
		    	var k = img.width/context.canvas.width + img.width/1000;
		    	context.canvas.width=img.width/k;
		    	context.canvas.height=img.height/k;
		    	// draw image
		        context.drawImage(img, 0, 0
		            , context.canvas.width, context.canvas.height
		        );
		    }

		    else if( img.height > context.canvas.height) {
		    	var k = img.height/context.canvas.height + image.width/1000;
		    	context.canvas.width=img.width/k;
		    	context.canvas.height=img.height/k;
		    	// draw image
		        context.drawImage(img, 0, 0
		            , context.canvas.width, context.canvas.height
		        );
		    }
	    	 else {
		    	// scale canvas to image
		        context.canvas.width = img.width;
		        context.canvas.height = img.height;
		        // draw image
		        context.drawImage(img, 0, 0
		            , context.canvas.width, context.canvas.height
		        );
	    	}
	    	
	    }
	    // this is to setup loading the image
	    reader.onloadend = function () {
	        img.src = reader.result;
	    }
	    // this is to read the file
	   	reader.readAsDataURL(file);
	}
}());

