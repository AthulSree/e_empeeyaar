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


    // $(document).on('click','.updateleaverecord', function(){
    //     var paidleaves = $(this).closest('tr').find('.paidleavedays').val();
    //     var non_paidleaves = $(this).closest('tr').find('.non_paidleavedays').val();
    //     var cand_id = $(this).data('candid');
    //     var path = $(this).data('path');

    //         var att_graph_meta = $(this).closest('tr').find('#att_graph')
    //         var att_details_meta = $(this).closest('tr').find('#att_details')
    //         att_graph = att_graph_meta[0].files[0]
    //         att_details = att_details_meta[0].files[0]

    //     console.log(att_graph, att_details);
    //     $.ajax({
    //         url : path,
    //         type : 'POST',
    //         data: { 'csrfmiddlewaretoken': csrf_token, paidleaves, non_paidleaves, cand_id, att_graph, att_details},
    //         success: function(response){
    //             // alert()
    //             leave_list();
    //         }
    //     })
    // })

    $(document).on('click', '.updateleaverecord', function () {
        var paidleaves = $(this).closest('tr').find('.paidleavedays').val();
        var non_paidleaves = $(this).closest('tr').find('.non_paidleavedays').val();
        var cand_id = $(this).data('candid');
        var path = $(this).data('path');

        var att_graph_meta = $(this).closest('tr').find('#att_graph');
        var att_details_meta = $(this).closest('tr').find('#att_details');
        var att_graph = att_graph_meta[0].files[0];
        var att_details = att_details_meta[0].files[0];

        var formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrf_token);
        formData.append('paidleaves', paidleaves);
        formData.append('non_paidleaves', non_paidleaves);
        formData.append('cand_id', cand_id);
        formData.append('att_graph', att_graph);
        formData.append('att_details', att_details);

        $.ajax({
            url: path,
            type: 'POST',
            data: formData,
            processData: false,  // Prevent jQuery from automatically transforming the data into a query string
            contentType: false,  // Let the browser set the content type, including the boundary for multipart/form-data
            success: function (response) {
                leave_list();
            },
            error: function (xhr, status, error) {
                console.error('Upload failed:', error);
            }
        });
    });


})