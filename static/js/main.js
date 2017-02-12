"use strict";

$(document).ready(function(){
  var post_id;
  var comment_id;
  var $selected_comment;
  var link;
  var delete_type;
  var comment;
  var initial_html = $('.container').html();

  $('#search-input').keyup(function(event){
    var text = $(this).val();
    if (!text){
      $('.container').html(initial_html);
    }
    else {
      $.get({
        url: '/search/' + text,
        success: function(data){
          $('.container').html(data)
        }
      })
    }
  })

  $('.slide-toggler').click(function(event){
    $('#full-description').slideToggle();
    $(this).children('.glyphicon').toggleClass("glyphicon-chevron-down")
    .toggleClass("glyphicon-chevron-up");
  })

  $('.post-del').click(function(event){
    link = $(this).data('link');
    post_id = $(this).attr('id').split('-')[1];
    delete_type = "post";
  });

  $('.comment-del').click(function(event){
    link = $(this).data('link');
    // id='comment-36' => comment_id=36
    $selected_comment = $(this).closest('.comment');
    comment_id = $selected_comment.attr('id').split('-')[1];
    delete_type = "comment";
  });

  $('.comments').on('click', '.com-edit', function(event){
    event.preventDefault();
    link = $(this).attr('href');
    console.log(link);
    var $comment = $(this).closest('.comment');
    console.log($comment);
    comment = $comment.prop('outerHTML');
    var content = $(this).parent().siblings('.com-content').text();
    $comment.replaceWith(
      "<form method='post' action='" + link + "'>\
        <textarea cols='88' id='id_content' maxlength='400' name='content' \
        rows='2' style='resize:none;' required=''>" + content + "</textarea>\
        <input class='btn btn-default align-right edit-btn' type='submit' value='Update'>\
        </input>\
        <div class='clear'></div>\
      </form>"

  )});

  $('.comments').on('click', '.edit-btn', function(event){
    event.preventDefault();
    var $form = $(this).closest('form');
    var content = $form.children('textarea').val();
    link = $form.attr('action');
    var regex = new RegExp('<p class="com-content">.*</p>', 'g');
    comment = comment.replace(regex, '<p class="com-content">' + content + '</p>');
    $.post(link, $form.serialize(), $form.replaceWith(comment));
  });

  $('.del-btn').click(function(event){

    $('#deleteModal').modal('hide')

    if (delete_type === "post"){
      $.ajax({
        type: 'POST',
        url: String(link),
        success: redirectToProfile(),
        async: false
      });
    }
    if (delete_type === "comment")
    {
      $.ajax({
        type: 'POST',
        url: String(link),
        success: function(data) {
          if (data.status == 'accepted'){
            $selected_comment.remove();
          }
        }
      })
    }
  });
});

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
