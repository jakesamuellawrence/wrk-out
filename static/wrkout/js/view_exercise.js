function hide_warning_dialogue() {
    $("#warning-container").css('display', 'none');
}

function show_warning_dialogue() {
    $("#warning-container").css('display', 'block');
}

$(document).ready(function() {
    $(".delete-button").click(show_warning_dialogue);
    $("#warning-container").click(hide_warning_dialogue);
    $("#warning-dialogue").click(function (event) {event.stopPropagation();});
    $("#delete-cancel").click(hide_warning_dialogue);
    $("#delete-confirm").click(function() {
        delete_url = window.location + "delete";
        $.ajax({
            url: delete_url,
            success: function(response) {
                window.location.href = "/";
            }
        });
    });
});