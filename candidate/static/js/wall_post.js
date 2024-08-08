

$(document).ready(function(){

  $('#imageDisplay').hide()
  poststat = $('#poststat').val();

  if(poststat == 200){
      const Toast = Swal.mixin({
          toast: true,
          position: "top-end",
          showConfirmButton: false,
          timer: 3000,
          timerProgressBar: true,
          didOpen: (toast) => {
            toast.onmouseenter = Swal.stopTimer;
            toast.onmouseleave = Swal.resumeTimer;
          }
        });
        Toast.fire({
          icon: "success",
          title: "Wall Post Updated"
        });
  }

  $(document).on('change','#uploadFile', function(){
      $('#imageDisplay').show()
      const fileInput = document.getElementById('uploadFile');
      const imageDisplay = document.getElementById('imageDisplay');
      const textarea = document.getElementById('content');
      
      // Remove any existing images in the imageDisplay div
      // imageDisplay.innerHTML = '';
      
      // Check if a file is selected
      if (fileInput.files.length > 0) {
          const file = fileInput.files[0];
          const reader = new FileReader();
          
          // Read the image file as a data URL
          reader.readAsDataURL(file);
          
          reader.onload = function(e) {
              const imageSrc = e.target.result;
              
              // Display the image in a div
              const imgElement = document.createElement('img');
              imgElement.src = imageSrc;
              imgElement.style.maxWidth = '100%';
              imgElement.style.height = 'auto';
              imageDisplay.appendChild(imgElement);
              
              // Set the image source directly into the textarea
              textarea.value = `<img src="${imageSrc}" alt="Uploaded Image">\n`;
          }
      } else {
          alert('Please select an image file.');
      }
  
  })


//   show msg for subjectless posts
  $(document).on('submit', '#formblockcontent', function(event) {
    event.preventDefault();

    var form = this; // Store a reference to the form
    var sub = $("#wp_subject").val();
    var reply_id = $("#wp_reply_id").val()

    if (sub == '' && reply_id == 0) {
        Swal.fire({
            title: "🤨",
            text: "Subject kodthaa sky idinj veezhuo ..? Humm!!!😒",
            backdrop: `rgba(0, 0, 0, 0.38) blur(10px) left top no-repeat`,
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Post anyway!"
        }).then((result) => {
            if (result.isConfirmed) { // Ensure that the user confirmed
                form.submit(); // Use the stored form reference to submit
            }
        });
    } else {
        // If there's a subject, submit the form immediately
        this.submit();
    }
});

// --------------delete posts
  $(document).on('click','.deleteWallPost', function(){
      postid = $(this).data('postid');
      deleteimgurl = $('#deleteconfirm').data('imgurl');
      successimgurl = $('#deletesuccess').data('imgurl');
      failedimgurl = $('#deletefailed').data('imgurl');
      path = $(this).data('deletepath');
      csrftoken = $('#csrf_token').val();

      if(postid == 1){
          Swal.fire("Can't delete")
          return false;
      }
      Swal.fire({
          title: "Are you sure?",
          text: "You won't be able to revert this!",
          imageUrl: deleteimgurl,
          imageWidth: 300,
          imageHeight: 300,
          imageAlt: "Custom image",
          backdrop: `rgba(0, 0, 0, 0.38) blur(10px) left top no-repeat`,    
          // icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Yes, delete it!"
        }).then((result) => {
          if (result.isConfirmed) {
              $.ajax({
                  url:path,
                  type: 'POST',
                  data:{'csrfmiddlewaretoken':csrftoken, postid},
                  success:function(data){
                      if(data.status==200){
                          Swal.fire({
                              title: "Deleted!",
                              text: "Your post has been deleted.",
                              icon: "success",
                              imageUrl: successimgurl,
                              imageWidth: 300,
                              imageHeight: 300
                            });
                      }else{
                          Swal.fire({
                              title: "Not deleted!",
                              text: "some error occurred.",
                              icon: "error",
                              imageUrl: failedimgurl,
                              imageWidth: 300,
                              imageHeight: 300    
                            });
                      }
                      setTimeout(() => {
                          window.location.reload();
                      }, 500);
                  }
              })
          }
        });
  })



  // ------- cpy to clipboard

  $(document).on('click','.wallpostcontent', function(){
      var content = $(this).text()
      console.log(content);
      var tempElement = $('<textarea>');
      tempElement.val(content);

      // Append the temporary element to the body
      $('body').append(tempElement);

      // Select the content of the textarea
      tempElement.select();

      // Execute the copy command
      document.execCommand('copy');

      // Remove the temporary element from the body
      tempElement.remove();

      // // Optionally, notify the user that the content has been copied
      // alert('Content copied to clipboard!');
      const Toast = Swal.mixin({
          toast: true,
          position: "bottom-left",
          showConfirmButton: false,
          timer: 3000,
          timerProgressBar: true,
          didOpen: (toast) => {
            toast.onmouseenter = Swal.stopTimer;
            toast.onmouseleave = Swal.resumeTimer;
          }
        });
        Toast.fire({
          icon: "success",
          title: "Content copied to clipboard"
        });
  })


//   -------- reply to wallpost

    $(document).on('click','.replyWallPost', function(){
        postid = this.dataset.postid;
        $("#wp_subject").hide();
        $("#uploadFile").hide();
        $("#imageDisplay").hide();
        $("#wp_sendto_ip").hide();
        $("#post_for").hide();
        $("#wp_reply_id").val(postid);
    })

    $(document).on('click','.post_item', function(){
        $("#wp_subject").show();
        $("#uploadFile").show();
        $("#imageDisplay").show();
        $("#wp_sendto_ip").show();
        $("#post_for").show();
        $("#wp_reply_id").val(0);
    })

})


