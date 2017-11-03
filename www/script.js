//BUZZ EFFECT BELONGS TO https://codepen.io/cRckls/
//###############################################
var showText = function (target, message, index, interval) {   
  if (index < message.length) {
    $(target).append(message[index++]);
    setTimeout(function () { showText(target, message, index, interval); }, interval);
  }
}
$(function () {
  showText("#msg", "Terminal", 0, 100);
  showText("#msg1", "My portfolio, type help", 0, 100);
});
 $(document).ready(function () {
            setTimeout("$('#messagetextarea').focus();", 500);
});
function checkforhelp(){
  if (document.getElementById('messagetextarea').value == "help") {
    showText("#msg2", 'commands:', 0, 100);
    var counter = 3;
	showText("#msg" + counter++, '#1 getxxlarge, get an extra extra large image', 0, 100);
	showText("#msg" + counter++, '#2 getxxlargegif, get an extra extra large gif', 0, 100);
	showText("#msg" + counter++, '#3 getxxx, get smut', 0, 100);
	showText("#msg" + counter++, '#4 bekommen, alias for get', 0, 100);
	showText("#msg" + counter++, '#5 gifbekommen, alias for getgif', 0, 100);
	showText("#msg" + counter++, '#6 giphy, get gif from giphy', 0, 100);
	showText("#msg" + counter++, '#7 imgur, get image from imgur', 0, 100);
	showText("#msg" + counter++, '#8 say, say something', 0, 100);
	showText("#msg" + counter++, '#9 add, add new commands', 0, 100);
	showText("#msg" + counter++, '#10 get, get an image', 0, 100);
	showText("#msg" + counter++, '#12 getfig, get an image of a fig', 0, 100);
	showText("#msg" + counter++, '#13 getgif, get a gif', 0, 100);
	showText("#msg" + counter++, '#14 gethuge, get a huge image', 0, 100);
	showText("#msg" + counter++, '#15 gethugegif, get a huge gif', 0, 100);
	showText("#msg" + counter++, '#16 getlarge, get a large image', 0, 100);
	showText("#msg" + counter++, '#17 getlargegif, get a large gif', 0, 100);
	showText("#msg" + counter++, '#18 getpic, get images of various sizes', 0, 100);
	showText("#msg" + counter++, '#19 getxlarge, get an extra large image', 0, 100);
	showText("#msg" + counter++, '#20 getxlargegif, get an extra large gif', 0, 100);
    document.getElementById('messagetextarea').value = '';
    return false; 
  }
  else{
    alert('redirecting...');
    return true;
  }

}

var textarea = document.querySelector('textarea');

textarea.addEventListener('keydown', autosize);
             
function autosize(){
  var el = this;
  setTimeout(function(){
    el.style.cssText = 'height:0; padding:0';
    el.style.cssText = 'height:' + el.scrollHeight + 'px';
  },0);
}
$(function() {
    $('textarea').on('keypress', function(e) {
        if (e.which == 32)
            return false;
    });
});
setTimeout(function(){
   $("textarea").text("LOADING TERMINAL");
},500); // 3 second delay



setTimeout(function(){
   $("textarea").text("STAND BY");
},2500); // 3 second delay


setTimeout(function(){
   $("textarea").text("SUCCESSFUL");
},5000); // 3 second delay


setTimeout(function(){
   $("textarea").text("");
},7000); // 3 second delay





