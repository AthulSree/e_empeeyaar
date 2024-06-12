
let menuicn = document.querySelector(".menuicn");
let nav = document.querySelector(".navcontainer");

menuicn.addEventListener("click", () => {
    nav.classList.toggle("navclose");
})


$(document).on('click', '.searchbtn,.dp', function () {
    alert('തെക്കോട്ട് നോക്കി ഇരുന്നോ');
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


