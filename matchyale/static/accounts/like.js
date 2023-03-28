var button = document.querySelector(".like_button");
button.classList.remove("animated");
button.addEventListener("click", function() {
button.classList.toggle("animated");
let like_text = document.querySelector('.like_text');


setTimeout(function(){
    
    button.classList.remove("animated");
    like_text.innerHTML = "Liked";
  
    
},1000);




});