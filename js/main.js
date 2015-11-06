// Base from: http://www.playfuljs.com/particle-effects-are-easy/
var DAMPING = 0.999;

function Particle(x, y) {
	this.x = this.oldX = x;
	this.y = this.oldY = y;
}

Particle.prototype.integrate = function() {
	var velocityX = (this.x - this.oldX) * DAMPING;
	var velocityY = (this.y - this.oldY) * DAMPING;
	this.oldX = this.x;
	this.oldY = this.y;
	this.x += velocityX;
	this.y += velocityY;
	if (Math.random() > 0.9)
	{
		this.x = this.oldX =  Math.random() * width;
		this.y = this.oldY = Math.random() * height;
	}
};

Particle.prototype.attract = function(x, y) {
	var dx = x - this.x;
	var dy = y - this.y;
	var distance = Math.sqrt(dx * dx + dy * dy);
	this.x += dx / distance;
	this.y += dy / distance;
};

Particle.prototype.draw = function() {
	ctx.strokeStyle = 'rgba(17,17,17,' + (Math.random() * 1.5) + ')';
	ctx.lineWidth = 2;
	ctx.beginPath();
	ctx.moveTo(this.oldX, this.oldY);
	ctx.lineTo(this.x, this.y);
	ctx.stroke();
};

var display = document.getElementById('phenomenon');
var ctx = display.getContext('2d');
var particles = [];
var width = display.width = $('.jumbotron').outerWidth();
var height = display.height = $('.jumbotron').outerHeight();
var mouse = { x: width * 0.5, y: height * 0.5 };

for (var i = 0; i < 200; i++) {
	particles[i] = new Particle(Math.random() * width, Math.random() * height);
}

display.addEventListener('mousemove', onMousemove);

function onMousemove(e)
{
    mouse.x = e.clientX;
    mouse.y = e.clientY;
}

requestAnimationFrame(frame);

function frame() {
    requestAnimationFrame(frame);
    ctx.clearRect(0, 0, width, height);
    for (var i = 0; i < particles.length; i++) {
        particles[i].attract(mouse.x, mouse.y);
        particles[i].integrate();
        particles[i].draw();
    }
}

function toggleMenu()
{
	$('.button').toggleClass('close');
	$('.menu').toggleClass('open');
	$('.chapterGroups').toggle();
	$('body').toggleClass('noscroll');
}

$('.button').click(function(){
	toggleMenu();
});

var chaptersContainer = $('.chapterGroups');
var currentChapterGroup = null;
var chapterCount = $('.titleContents').length
for (var i = 1; i <= chapterCount; i = i + 1)
{
	if ( i % 10 === 1 )
	{
		var upper = i + 9;
		upper = (upper >= chapterCount) ? chapterCount : upper;
		currentChapterGroup = $('<div />', {
			"class": 'chapterGroup'
		});

		currentChapterGroup.append($('<div />', {
			text: i + '-' + upper,
			group: i + '-' + upper,
			"class": "ChapterGroupLabel"
		}));

		var chapterGroupCell = $('<div />', {
			"class": 'chapterGroupCell col-md-2 col-sm-3 col-xs-4'
		});

		chapterGroupCell.append(currentChapterGroup);
		chaptersContainer.append(chapterGroupCell);
	}

	var chapterCell = $('<div />', {
		"class": 'chapterCell col-md-2 col-sm-3 col-xs-4'
	});
	var chapter = $('<div />', {
		"class": 'chapter',
		text: i,
		chapter: i
	});

	chapterCell.append(chapter)
	currentChapterGroup.append(chapterCell);
}

function ToggleChapterGroupCell(group)
{
	$(group).find(".chapterCell").toggle();
	$(group).toggleClass('open');
	$('.chapterGroupCell').not(group).toggle();
}

$('.ChapterGroupLabel').click(function(e){
	e.stopPropagation();
	$chapterGroupCell = $(this).parent().parent();
	if ($chapterGroupCell.hasClass('open'))
	{
		$(this).text($(this).attr("group"));
	}
	else
	{
		$(this).text("⬅");
	}
	ToggleChapterGroupCell($chapterGroupCell);
});

$('.chapterGroupCell').click(function(){
	ToggleChapterGroupCell(this);
})

$('.chapter').click(function(e){
	e.stopPropagation();
	$(this).parent().siblings('.ChapterGroupLabel').click();
	toggleMenu();
	window.location.hash = $(this).attr("chapter");
});
