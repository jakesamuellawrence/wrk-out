$(document).ready(function () {
    $(".add-exercise-button").click(function() {
        trashImgSource = $(this).data("trash-src");
        exerciseSlug = $(this).data("exercise-slug")
        exerciseHref = $(this).data("exercise-href");
        exerciseName = $(this).data("exercise-name");

        $("#selected-exercise-list").append(`
        <div class="selected-exercise-row">
            <a href="${exerciseHref}">${exerciseName}</a>
            x <input type="number" min="1" name="${exerciseSlug}" value="1">
            <img class="remove-exercise-button" src="${trashImgSource}">
        </div>
        `);

        $(".remove-exercise-button").click(function () {
            console.log("being clicked!");
            $(this).closest(".selected-exercise-row").remove();
        })
    });
});