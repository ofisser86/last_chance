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

$(document).ready(function () {
    initJournal();
});