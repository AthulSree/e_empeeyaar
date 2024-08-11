$(document).ready(function () {
    // fetching own folders
    load_own_folders();

    // loading own folders
    function load_own_folders() {
        var csrf_token = $('#csrf_token').val()
        var path = $('#own_folder_chamber').data('url');
        console.log(csrf_token);
        $.ajax({
            url: path,
            type: "POST",
            data: { 'csrfmiddlewaretoken': csrf_token },
            success: function (data) {
                $('#own_folder_chamber').html(data)
            }
        })
    }


    $(document).on('click', '#file_upload', function () {
        loadmodal('myModal')
    })
    $(document).on('click', '#new_folder', function () {
        $('.newfolderdom').show();
        $('.renamefolderdom').hide();
        loadmodal('newFolderModal')
    })


    // saving new folder
    $(document).on('submit', '#newFolderForm', function (e) {
        e.preventDefault()
        path = this.dataset.action
        var formdata = new FormData(this);
        console.log(path);

        $.ajax({
            url: path,
            type: "POST",
            data: formdata,
            processData: false,
            contentType: false,
            success: function (data) {
                // swal(data.status,data.msg,data.status)
                toastmessage(data.status, data.msg)
                load_own_folders();
                $('.closemodal').trigger('click')
            }
        })

    })

    $(document).on('click', '#main-button-docs', function () {
        $('.floating-btn-docs').toggleClass('active')
    })

    // setTimeout(openFirstAlert, 1000);
    function openFirstAlert() {
        Swal.fire({
            title: 'Ethayalum vannille...',
            input: 'textarea',
            // inputLabel: 'Let me know your feedback about byte-WhaSsh',
            html: `<label for="swal-input1" style="display: block; margin-bottom: 10px;">
							Let me know your feedback about <i>byte-WhaSsh</i>
							</label>`,
            inputPlaceholder: 'Type your message here...',
            inputAttributes: {
                'aria-label': 'Type your message here'
            },
            showCancelButton: true,
            confirmButtonText: 'Save',
            cancelButtonText: 'Parayoola!',
            preConfirm: function (message) {
                if (!message) {
                    Swal.showValidationMessage('Please enter a message... Enter chey monu :)');
                    return false;
                }
                return message;
            }
        }).then(function (result) {
            if (!result.isConfirmed) {
                Swal.fire({
                    title: 'Aahaa! 🤨',
                    text: "Paranjitt poyaa mathi",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Parayaam',
                    cancelButtonText: 'Enthayalum Parayaam',
                }).then(function () {
                    openFirstAlert();
                });
            } else {

                my_ip = $("#id_myip").val();
                path = $("#id_myip").data('path');
                feedback = result.value;
                var csrf_token = $('#csrf_token').val();
                $.ajax({
                    url: path,
                    type: 'POST',
                    data: { 'csrfmiddlewaretoken': csrf_token, 'feedback': feedback, 'my_ip': my_ip },
                    success: function (data) {
                        Swal.fire({
                            title: 'Good Boy',
                            text: 'Tengz🙂',
                            icon: 'success'
                        });
                    }

                })
            }
        });
    }



    $(document).on('click', '.dropdown-item', function () {
        var ddtype = this.dataset.ddtype;
        var fid = this.dataset.fid;
        var name = this.dataset.name;

        if (ddtype === "rename_folder") {
            $('form').on('keypress', function (e) {
                if (e.which === 13) { // 13 is the Enter key
                    e.preventDefault();
                    return false;
                }
            });
            $("#docs_folderName").val(name);
            $('.newfolderdom').hide();
            $('.renamefolderdom').show();
            loadmodal('newFolderModal');

            // Set up the save button click handler
            $('#renameFolder').off('click').on('click', function () {
                var newName = $('#docs_folderName').val();
                performAjaxRequest(ddtype, fid, newName); // Use the common AJAX function
            });
        } else {
            performAjaxRequest(ddtype, fid); // Use the common AJAX function for other cases
        }
    });


    // Common AJAX function
    function performAjaxRequest(ddtype, fid, newName = null) {
        var path = $("#folderedit_url").val();
        var csrfmiddlewaretoken = $('#csrf_token').val();

        var data = {
            csrfmiddlewaretoken,
            ddtype,
            fid
        };

        if (newName !== null) {
            data.newName = newName;
        }

        $.ajax({
            url: path,
            type: "POST",
            data: data,
            success: function (data) {
                toastmessage(data.status, data.msg);
                load_own_folders();
                $('.closemodal').trigger('click');
            },
            error: function (error) {
                console.error('Error performing AJAX request:', error);
            }
        });
    }



    // drag and drop files--------------------

    var formData = new FormData();


    var dropzone = $('#dropzone');
    var fileInput = $('#fileInput');
    var fileList = $('#fileList');

    // Open file dialog on dropzone click
    dropzone.on('click', function () {
        fileInput.click();
    });

    // Handle file selection via input
    fileInput.on('change', function (e) {
        handleFiles(e.target.files);
    });

    // Handle dragover event
    dropzone.on('dragover', function (e) {
        e.preventDefault();
        e.stopPropagation();
        dropzone.addClass('dragover');
    });

    // Handle dragleave event
    dropzone.on('dragleave', function (e) {
        e.preventDefault();
        e.stopPropagation();
        dropzone.removeClass('dragover');
    });

    // Handle drop event
    dropzone.on('drop', function (e) {
        e.preventDefault();
        e.stopPropagation();
        dropzone.removeClass('dragover');
        var files = e.originalEvent.dataTransfer.files;
        handleFiles(files);
    });

    // Function to handle file upload
    function handleFiles(files) {
        // Clear the file list
        fileList.empty();

        // Loop through each file and append its name to the list
        $.each(files, function (index, file) {
            formData.append('files[]', file);
            fileList.append('<li>' + file.name + '</li>');
        });
    }


    $(document).on('click', '#saveFiles', function () {
        console.log(formData);
    })


})