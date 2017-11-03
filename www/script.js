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
            setTimeout("$('#fname').focus();", 500);
});
function checkforblank(){
  if (document.getElementById('fname').value == "help") {
    
    showText("#msg2", 'commands:', 0, 100);
	showText("#msg3", '#1 getxxlarge, get an extra extra large image', 0, 100);
	showText("#msg4", '#2 getxxlargegif, get an extra extra large gif', 0, 100);
	showText("#msg5", '#3 getxxx, get smut', 0, 100);
	showText("#msg6", '#4 bekommen, alias for get', 0, 100);
	showText("#msg7", '#5 gifbekommen, alias for getgif', 0, 100);
	showText("#msg8", '#6 giphy, get gif from giphy', 0, 100);
	showText("#msg9", '#7 imgur, get image from imgur', 0, 100);
	showText("#msg10", '#8 say, say something', 0, 100);
	showText("#msg11", '#9 add, add new commands', 0, 100);
	showText("#msg12", '#10 get, get an image', 0, 100);
	showText("#msg13", '#12 getfig, get an image of a fig', 0, 100);
	showText("#msg14", '#13 getgif, get a gif', 0, 100);
	showText("#msg15", '#14 gethuge, get a huge image', 0, 100);
	showText("#msg16", '#15 gethugegif, get a huge gif', 0, 100);
	showText("#msg17", '#16 getlarge, get a large image', 0, 100);
	showText("#msg18", '#17 getlargegif, get a large gif', 0, 100);
	showText("#msg19", '#18 getpic, get images of various sizes', 0, 100);
	showText("#msg20", '#19 getxlarge, get an extra large image', 0, 100);
	showText("#msg21", '#20 getxlargegif, get an extra large gif', 0, 100);
    
    //(document.getElementById('textarea').document.write('jajajajajjaja'());

    return false; 
  }
  else{
    alert('error: "help", dont have space at the end');
    return false;
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





