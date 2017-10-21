function initJournal() {
    var indicator = $('#ajax-progress-indicator');
    var ajaxerror = $('#errJournalSave').hide();
    $('.day-box input[type="checkbox"]').click(function (event) {
        var box = $(this);
        $.ajax(box.data('url'), {
           'type': 'POST',
           'async':true,
           'dataType': 'json',
           'data':{
               'pk':box.data('student-id'),
               'date':box.data('date'),
               'present':box.is(':checked') ? '1' : '',
               'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
           },
            'beforeSend': function (xhr, settings) {
                indicator.show();
                ajaxerror.hide();
            },
            'error': function (xhr, status, error) {
               indicator.hide();
               ajaxerror.show().addClass('.alert alert-danger').append(error);
            },
            'success': function (data, status, xhr) {
               indicator.hide();
               ajaxerror.hide();
            }
        });
    });
}

function initGroupSelection() {
    // look up select element with groups and attach our even handler
    // on field ”change” event
    $('#group-selector select').change(function (event) {
        // get value of currently selected group option
        var group = $(this).val()

        if (group){
            // set cookie with expiration date 1 year since now;
            // cookie creation function takes period in days
            $.cookie('current_group', group, {'path':'/', 'expires':365});
        }
        else {
            // otherwise we delete the cookie
            $.removeCookie('current_group', {'path': '/'});
        }
            // and reload a page
            location.reload(true);

            return true;
    });
}

$(document).ready(function () {
    initJournal();
    initGroupSelection();
});