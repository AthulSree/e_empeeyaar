
let menuicn = document.querySelector(".menuicn");
let nav = document.querySelector(".navcontainer");

menuicn.addEventListener("click", () => {
    nav.classList.toggle("navclose");
})


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


