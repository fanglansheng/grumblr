
function populateComments(){
    // generate comments
    $.get("/grumblr/getCommentLists")
        .done(function(data){
            for(var i = 0; i < data.comments.length; i++){
                var commentList = data.comments[i];
                var newComments = $(commentList.html);
                // get postItem
                var postId = commentList.postId;
                var curPost = $('#'+postId+' .comment-contianer');
                curPost.prepend(newComments);
            var postList = $("#posts-list");
            postList.data('commentMax', data['maxCount']);
            console.log(data['maxCount']);
        }
    });

}


function updateComments(){
    var postList = $("#posts-list");
    var commentMax = postList.data("commentMax");
    $.get("/grumblr/getCommentChanges/"+commentMax)
        .done(function(data) {
            postList.data('commentMax', data['maxCount']);
            // console.log(data.posts);
            for(var i = 0; i < data.comments.length; i++){
                var commentList = data.comments[i];
                var newComments = $(commentList.html);
                // get postItem
                var postId = commentList.postId;
                var curPost = $('#'+postId+' .comment-contianer');
                curPost.append(newComments);
          }
        }); 
}

function addComment(){
  // get current focus comment input
  var commentInput = $('.comment-post:focus');
  var post_id = commentInput.data("postId");
  console.log(post_id);
  $.post("/grumblr/add_comment/"+post_id, {content: commentInput.val()})
      .done(function(data) {
        console.log("===");
          updateComments();
          commentInput.val("").focus();
      });

}


$(document).ready(function () {
    // add event-handler to dynamic created items
    $("#posts-list").on("keypress",".comment-post", 
      function (e) { if (e.which == 13) addComment(); } );

    // Periodically refresh to-do list
    window.setInterval(updateComments, 5000);

    populateComments();

    // CSRF set-up copied from Django docs
    function getCookie(name) {  
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
    });

});
