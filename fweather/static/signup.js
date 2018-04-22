$(function () {
    $('#subscribe-form').on('submit', function(e) {
        // skip form redirection
        e.preventDefault();
        // send an ajax post instead
        $.post('/signup',  $(this).serialize())
            .done(function(data) {
                var msg = $('#messages');
                if (data.success === true) {
                    msg.attr('class', 'alert alert-success');
                } else {
                    msg.attr('class', 'alert alert-danger');
                }
                msg.text(data.msg);
            });
        return false;
    });
});