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
  showText("#msg1", "type help", 0, 100);
});
 $(document).ready(function () {
  setTimeout("$('#messagetextarea').focus();", 500);
});
function checkforhelp(){
  $('#messagetextarea').focus();
  if (document.getElementById('messagetextarea').value.toLowerCase() == "help") {
    var xhttp = new XMLHttpRequest();
    var commandList = [];
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        showAllCommandText(this.responseText);
      }
    };
    xhttp.open("GET", "/list_commands", true);
    xhttp.send();
  } else {
    var xhttp = new XMLHttpRequest();
    var commandList = [];
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        showCommandText(this.responseText);
      }
    };
    xhttp.open("GET", "/webhook", true);
    xhttp.send();
  }
}
function showCommandText(commandList){
  showText("#msg1", commandList, 0, 100);
}
function showAllCommandText(commandList){
  var commandsObject = JSON.parse(commandList)
  for (counter = 0; counter < commandsObject.length; counter++) {
    showText("#msg" + (counter+3), '#' + (counter+1) + ' ' + commandsObject[counter] + ', command_description_here', 0, 100);
  }
}

$(document).keypress(function(e) {
	if(e.which == 13) {
      event.preventDefault();
      if (checkforhelp()) {
        $("executecommandform").submit();
      }
    }
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



