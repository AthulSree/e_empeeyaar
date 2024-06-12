$(document).ready(function(){

    leave_list()

    function leave_list(){
        path = $('#leave_update_list').val();
        csrf_token = $('#csrf_token').val();
        $.ajax({
            url:path,
            type:'POST',
            data:{'csrfmiddlewaretoken' : csrf_token},
            success:function(html){
                $('#leaveUpdate_list_table').html(html)
            }
        })
    }



    $(document).on('click','.editleaverecord',function(){
        $(this).closest('tr').find('.leaveentry').show()
        $(this).closest('tr').find('.leavelabel').hide()
        $(this).hide()
        $(this).closest('td').find('.updateleaverecord').show()
        var paidleaves = $(this).data('paidleaves') == 'None' ? '' : $(this).data('paidleaves')
        var nonpaidleaves = $(this).data('nonpaidleaves') == 'None' ? '' : $(this).data('nonpaidleaves')
        
        $(this).closest('tr').find('.paidleavedays').val(paidleaves);
        $(this).closest('tr').find('.non_paidleavedays').val(nonpaidleaves);
        $(this).closest('tr').find('.paidleavedays').focus();
    })


    $(document).on('click','.updateleaverecord', function(){
        var paidleaves = $(this).closest('tr').find('.paidleavedays').val();
        var non_paidleaves = $(this).closest('tr').find('.non_paidleavedays').val();
        var cand_id = $(this).data('candid');
        var path = $(this).data('path');

        console.log(paidleaves,non_paidleaves,cand_id);
        $.ajax({
            url : path,
            type : 'POST',
            data: { 'csrfmiddlewaretoken': csrf_token, paidleaves, non_paidleaves, cand_id},
            success: function(response){
                // alert()
                leave_list();
            }
        })
    })

})