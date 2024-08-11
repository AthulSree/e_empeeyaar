
function loadmodal(modal_id) {
    var modal = $('#'+modal_id+'')

    var closeModalBtn = $('.closemodal');

    modal.css('display', 'block');
    $('body').addClass('modal-active');

    // Listen for close click
    closeModalBtn.on('click', function () {
        modal.css('display', 'none');
        $('body').removeClass('modal-active');
    });

    // Close modal if user clicks outside of the modal content
    $(window).on('click', function (event) {
        if ($(event.target).is(modal)) {
            modal.css('display', 'none');
            $('body').removeClass('modal-active');
        }
    });
}
