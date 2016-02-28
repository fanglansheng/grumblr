function populateList() {
    $.get("/grumblr/stream/getPosts")
      .done(function(data) {
        var postList = $("#posts-list");
        // store posts data from json to postList element
        postList.data('maxCount', data['maxCount']);
        // empty the current postList content to create new posts.
        postList.html('');
        // create new posts
        for (var i = 0; i < data.posts.length; i++) {
            var post = data.posts[i];
            var new_item = $(post.html);
            postList.append(new_item);
            $('#'+post.postId+' .comment-post').data("postId",post.postId);
        }
        
      });
}

function populateComments(){
    // generate comments
    $.get("/grumblr/getCommentLists")
        .done(function(data){
            var postList = $("#posts-list");
            postList.data('commentMax', data['maxCount']);
            console.log(postList.data('commentMax'));
            for(var i = 0; i < data.comments.length; i++){
                var commentList = data.comments[i];
                var newComments = $(commentList.html);
                // get postItem
                var postId = commentList.postId;
                var curPost = $('#'+postId+' .comment-contianer');
                curPost.prepend(newComments);
            
        }
    });

}

function updateList(){
    var postList = $("#posts-list");
    var maxEntry = postList.data("maxCount");

    $.get("/grumblr/stream/getChanges/"+maxEntry)
    .done(function(data) {
      postList.data('maxCount', data['maxCount']);
      // console.log(data.posts);
      // alert("");
      for (var i = 0; i < data.posts.length; i++) {
          var post = data.posts[i];
          var new_item = $(post.html);
          postList.prepend(new_item);
          $('#'+post.postId+' .comment-post').data("postId",post.postId);
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

function addItem(){
    var postForm = $("#postform");
    $.ajax({ 
        type: postForm.attr('method'), 
        url: postForm.attr('action'), 
        data: postForm.serialize(),
    })
        .done(function(data) {
            console.log("hdfadf");
            if(data.type == "error"){
                errMsg = "";
                $.each(data.content,function(i,el){
                    console.log(i);
                    errMsg +=el[0].message;
                    console.log(errMsg);
                    // $(".registerError").html(function(0, "sdff"));
                    // function(0, el[0].message)
                });
                $('[data-toggle="tooltip"]').tooltip();  
                $("#post-text-area").addClass("post-warning");
            }
            else{
              $('[data-toggle="tooltip"]').tooltip('disable');
              $("#post-text-area").removeClass("post-warning");
                updateList();
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
          updateComments();
          commentInput.val("").focus();
      });

}


$(document).ready(function () {
    // Add event-handlers
    $("#post-btn").click(function(ev){
        ev.preventDefault();
        addItem();
    });
    // add event-handler to dynamic created items
    $("#posts-list").on("keypress",".comment-post", 
      function (e) { if (e.which == 13) addComment(); } );

    // Set up post list with initial DB items and DOM data
    populateList();
    populateComments();

    // Periodically refresh to-do list
    window.setInterval(updateList, 5000);
    window.setInterval(updateComments, 5000);

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
