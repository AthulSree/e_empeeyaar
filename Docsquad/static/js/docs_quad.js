$(document).ready(function(){
    alert();


    $(document).ready(function () {
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
                        Swal.showValidationMessage('Please enter a message');
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
                    // console.log(result.value);
                    // console.log(path,feedback,my_ip);
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

        // openFirstAlert();
    //    setTimeout(openFirstAlert, 1000);
    });

})