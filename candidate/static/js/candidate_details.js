$(document).ready(function(){
    
    fetch_all_candidates()
    $('.passwordblock').hide();
    $('.formblockcontent').show();
    $('.updatecandidate').hide();

    pagestat = $('#id_pagestat').val();
    if(pagestat == '200'){
        showToast('Successfully Updated','green');
    } else if (pagestat == '500'){
        showToast('Error occurred! Odikko','red');
    }

    // -----fetching all candidate details
    function fetch_all_candidates(){
        var path = $('#show_all_candidates').data('viewallurl');
        var csrf_token = $('#csrf_token').val();
        $.ajax({
            url:path,
            type:'POST',
            data: {
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (result) {
                $('#show_all_candidates_table').html(result)
                $('#allcandidatedetails').DataTable()

            }
        })
    }

    // -----password check for update
    $(document).on('click','#pass_check',function(){
        var inpPass = $('#inputPassword').val();
        // if(inpPass == 'adichkerivaa'){
        if(inpPass == ''){
            $('.passwordblock').hide();
            $('.formblockcontent').show();
        }else{
            $('#id_addNewAccordion').trigger('click')
        }
        $('#inputPassword').val('');
    })

    // -----edit candidate details
    $(document).on('click','.editcandidate', function(){
        $('.formblockcontent').hide();
        $('.passwordblock').show();
        $('#inputPassword').focus();
        $('.updatecandidate').show();
        $('.addcandidate').hide();
        $('#id_cand_addmode').val('edit')

        c_id = $(this).data('candid');
        classname = $('#AddNewAccordion').attr('class')
            if(classname == 'collapse'){
                $('#id_addNewAccordion').trigger('click')
            }

        var candidate_details = [];
        $row = $(this).closest('tr');
        $row.find('td').each(function(){
            candidate_details.push($(this).text());
        })
        var date = new Date(candidate_details[5]);
        var formattedjoiningDate = date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2);
        $('#id_cand_id').val(c_id)
        $('#id_cand_name').val(candidate_details[0])
        $('#id_cand_desig').val(candidate_details[1])
        $('#id_cand_wonumber').val(candidate_details[2])
        $('#id_cand_proj_num').val(candidate_details[3])
        $('#id_cand_join_date').val(formattedjoiningDate)
    })


})