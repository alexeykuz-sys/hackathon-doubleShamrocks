$(document).ready(function(){
  /**
   *  Initializes Bootstrap toasts
   */
  $('.toast').toast('show');
});





function uploading(){
  document.getElementById("overlay").style.display = "block";
}

function off() {
  document.getElementById("overlay").style.display = "none";
};