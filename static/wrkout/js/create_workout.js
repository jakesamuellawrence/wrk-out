$(document).ready(function () {
    $(".add-exercise-button").click(function() {
        trashImgSource = $(this).data("trash-src");
        exerciseSlug = $(this).data("exercise-slug");
        exerciseHref = $(this).data("exercise-href");
        exerciseName = $(this).data("exercise-name");

        $("#selected-exercise-list").append(`
        <div class="selected-exercise-row">
            <a href="${exerciseHref}">${exerciseName}</a>
            <input type="hidden" name="exerciseSlugs" value="${exerciseSlug}"/>
            x <input type="number" min="1" name="NoOfReps" value="1">
            <img class="remove-exercise-button" src="${trashImgSource}">
        </div>
        `);

        $(".remove-exercise-button").click(function () {
            $(this).closest(".selected-exercise-row").remove();
        });
    });

    $("#exercise-selector-search").on('input', function () {
        rows = $("#exercise-selector-list").children(".exercise-selector-row");

        searchKey = $(this)[0].value.trim().toLowerCase();

        for (i = 0; i < rows.length; i++) {
            exerciseName = $(rows[i]).children("a")[0].innerHTML;
            if (exerciseName.toLowerCase().trim().includes(searchKey)) {
                $(rows[i]).css("display", "flex");
            } else {
                $(rows[i]).css("display", "none");
            }
        }
    });
});