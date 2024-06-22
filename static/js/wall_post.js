

$(document).ready(function(){
    $('#imageDisplay').hide()

    $(document).on('change','#uploadFile', function(){
        $('#imageDisplay').show()
        $('#imageDisplay').text('Please wait....Image is uploading...')
        const fileInput = document.getElementById('uploadFile');
        const imageDisplay = document.getElementById('imageDisplay');
        const textarea = document.getElementById('content');
        
        // Remove any existing images in the imageDisplay div
        imageDisplay.innerHTML = '';
        
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



    $(document).on('click','#save_wall_post', function(){

    })


})


