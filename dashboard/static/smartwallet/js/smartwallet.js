$(document).ready(function(){
 
    $('.message a').click(function(){
        $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
    });
    
});

$(document).ready(function() {
  $('.js-spinner').click(function() {
      $(this).innerHTML = "<i class=\"fas fa-spinner\"></i>"
    $(this).addClass('icn-spinner') //remove class to stop animation
  });
});