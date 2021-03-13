// Display or not range inputs for columns
$("#id_type").on("click", () => {
    switch ($("#id_type").val()) {

        case "Integer":
            $("#hide3").attr({ "class": "col" });
            $("#hide4").attr({ "class": "col" });
            break;

        default:
            $("#hide3").attr({ "class": "col d-none" });
            $("#hide4").attr({ "class": "col d-none" });
    }
});


// Sends AJAX request to backend and append new column element to the page
$("#createColumn").submit(function (e) {
    e.preventDefault();

    $.ajax({
        type: "POST",
        url: "/new/column/",
        data: $(this).serialize()
    })
    .done((response) => {
        $("#createColumn").trigger('reset');

        let notShow;
        switch (response.type) {

            case "Integer":
                notShow = "";
                break

            default:
                notShow = "not-show";
        }

        $("#columnRows").append(
            `<form class="columnRow" action="/column/delete/${response.id}/" method="POST">
                <input type="hidden" name="csrfmiddlewaretoken" value="${response.csrfmiddlewaretoken}">
                <div class="row mb-3">
                    <div class="col">
                        <label  class="form-label">Column name</label>
                        <input type="text" class="form-control" readonly placeholder="${response.name}">
                    </div>
                    <div class="col">
                        <label  class="form-label">Type</label>
                        <input type="text" class="form-control" readonly placeholder="${response.type}">
                    </div>
                    <div class="col ${notShow}">
                        <label class="form-label">From</label>
                        <input type="text" class="form-control" readonly placeholder="${response.start}">
                    </div>
                    <div class="col ${notShow}">
                        <label class="form-label">To</label>
                        <input type="text" class="form-control" readonly placeholder="${response.end}">
                    </div>
                    <div class="col-1">
                        <button type="submit" class="btn btn-danger col-submit">Delete</button>
                    </div>
                </div>
            </form>`
        );
    })
    .fail((err) => {
        return false;
    })
});

// Send AJAX request for removal column to backend and remove element from the page.
$("#columnRows").on("submit", ".columnRow", function(e) {
    e.preventDefault();

    $.ajax({
        type: "POST",
        url: `${this.action}`,
        headers: {
            "X-CSRFToken": $(this).find("input[name='csrfmiddlewaretoken']").val()
        }
    })
    .done((response) => {
        $(this).remove();
    })
    .fail((err) => {
        return false;
    })
});

// Send AJAX request to create new dataset and append it to the page.
$("#dataSetCreate").submit(function (e) {
    e.preventDefault();

    $.ajax({
        type: "POST",
        url: `${this.action}`,
        data: $(this).serialize()
    })
    .done((response) => {
        $("#dataSetSubmit").prop("disabled", true);
        $("tbody").append(
            `
            <tr>
                <th class="align-middle" scope="row">
                    ${response.count}
                </th>
                <td class="align-middle">
                    ${response.created}
                </td>
                <td class="align-middle">
                    <div class="btn btn-danger taskStatus">${response.status}</div>
                </td>
                <td>
                    <form id="getFile" action="/schema/get_file/${response.dataset_id}/" method="get">
                        <button class="btn btn-outline-warning disabled downloadButton" type="submit">Download</button>
                    </form>
                </td>
            </tr>
            `
        )
        getTaskStatus(response.task_id);
    })
    .fail((err) => {
        return false;
    })
})

// Send AJAX request to backend to check CSV file creation task status
function getTaskStatus(task_id) {
    $.ajax({
        type: "GET",
        url: `/tasks/${task_id}/`
    })
    .done((response) => {
        const taskStatus = response.task_status;
        const taskID = response.task_id;

        switch (taskStatus) {
            case "SUCCESS":
                $(".taskStatus").last().attr("class", "btn btn-success taskStatus");
                $(".taskStatus").last().html("Ready");
                $(".downloadButton").last().attr("class", "btn btn-warning downloadButton");
                $("#dataSetSubmit").prop("disabled", false);
                $("#dataSetCreate")[0].reset();
                break;

            case "PENDING":
                setTimeout(() => {
                    getTaskStatus(taskID)
                }, 1000);
                break;

            default:
                return false;
        }
    })
    .fail((err) => {
        console.log(err);
    })
}

// Check if almost one column was added
$("#createSchemaButton").on('click', function (e) {
    if ($(".columnRow").length === 0) {
        e.preventDefault()
    }
})


// Send AJAX request to backend to delete schema and remove it from page.
$(".deleteSchema").submit(function (e) {
    e.preventDefault();

    $.ajax({
        type: "POST",
        url: `${this.action}`,
        headers: {
            "X-CSRFToken": $(this).find("input[name='csrfmiddlewaretoken']").val()
        }
    })
    .done((response) => {
        $(this).parent().parent().remove();

        let schemaRows = $(".schemaCounter");
        for (let count = 1; count <= schemaRows.length; count++) {
            $(schemaRows[count-1]).text(count);
        }
    })
    .fail((err) => {
        console.log(err);
    })
})
