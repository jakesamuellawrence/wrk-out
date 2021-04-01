function hide_warning_dialogue() {
    $("#warning-container").css('display', 'none');
}

function show_warning_dialogue() {
    $("#warning-container").css('display', 'block');
}

$(document).ready(function() {

    href = "";

    $(".delete-button").click(function() {
        show_warning_dialogue();
        href = $(this).data("href");
    });
    $("#warning-container").click(hide_warning_dialogue);
    $("#warning-dialogue").click(function (event) {event.stopPropagation();});
    $("#delete-cancel").click(hide_warning_dialogue);
    $("#delete-confirm").click(function() {
        delete_url = href + "delete";
        $.ajax({
            url: delete_url,
            success: function(response) {
                window.location.href = window.location;
            }
        });
    });
    $(".collection-remove-button").click(function() {
        console.log("test!");
        unsave_url = $(this).data("href") + "unsave";
        $.ajax({
            url: unsave_url,
            success: function(response) {
                window.location.href = window.location;
            }
        });
    });
});