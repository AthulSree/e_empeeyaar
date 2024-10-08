

var unReadcount = $("#unReadAvail").val();
if(unReadcount == 0){
    $("#pulldown-image").hide();
}

$(document).on('click', '.searchbtn,.dp', function () {
    alert('തെക്കോട്ട് നോക്കി ഇരുന്നോ');
})

$(document).on('change','#id_curr_month',function(){
    var path = $(this).data('path')
    var month = $(this).val();
    var csrf_token = $('#csrf_token').val();
    $.ajax({
        url: path,
        type: 'POST',
        data: {'csrfmiddlewaretoken':csrf_token, month},
        success: function(status){
            if(status['status'] == 200){
                window.location.reload();
            }
        }
    })
})

$(document).on('click','.pdf_print', function(){
    mprprint = $(this).hasClass('mprprint')
    pdftypeEle = $(this).closest('form').find('#id_pdftype')
    if(mprprint){
        pdftypeEle.val('mpr')
    }else{
        pdftypeEle.val('lac')
    }
})


$(document).on('click','#send_whatsapp_msg',function(){
    path = $(this).data('url')
    var csrf_token = $('#csrf_token').val();
    $.ajax({
        url:path,
        type:'post',
        data: { 'csrfmiddlewaretoken': csrf_token },
        success: function (status) {
            if(status['status']==400){
                showToast('Message send successfully','green')
            }
        }
    })
})


$(document).on('click','#processpdf',function(){
    path = $(this).data('path')
    var csrf_token = $('#csrf_token').val();
    $.ajax({
        url: path,
        type: 'post',
        data: { 'csrfmiddlewaretoken': csrf_token },
        success: function (status) {
            console.log(status);
            if (status['status'] == 200) {
                showToast('PDFs renamed Successfully', 'green')
            }else{
                showToast('PDFs rename thenjirikkanu !!! :(', 'red')
            }
        }
    })
})



function showToast(message, bgColor = '#333') {
    const toastContainer = $('#toast-container');
    const toast = $('<div class="toast"></div>').text(message).css('background-color', bgColor);

    toastContainer.append(toast);

    setTimeout(() => {
        toast.addClass('show');
        setTimeout(() => {
            toast.removeClass('show');
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    }, 100);
}


function toastmessage(type, msg) {
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
        icon: type,
        title: msg
    });

}


