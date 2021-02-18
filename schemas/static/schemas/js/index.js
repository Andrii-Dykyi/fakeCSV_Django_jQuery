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

$("#createColumn").submit(function (e) {
    e.preventDefault();

    $.ajax({
        type: "POST",
        url: "/new_column/",
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
            `<form class="columnRow" action="/new_column/delete/${response.id}/" method="POST">
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


$("#dataSetCreate").submit(function (e) {
    e.preventDefault();

    $.ajax({
        type: "POST",
        url: `${this.action}`,
        data: $(this).serialize()
    })
    .done((response) => {
        console.log(response);
    })
    // TODO
})

// function getTaskStatus(task_id, report_pk) {
//     $.ajax({
//         type: "GET",
//         url: `/reports/tasks/${task_id}/`,
//         success: (response) => {
//             const taskStatus = response.task_status;
//             const taskID = response.task_id
//             console.log(taskStatus, taskID);

//             if (taskStatus === "SUCCESS") {
//                 $("#reportGet").attr('action', `/reports/get_report/${report_pk}/`);
//                 $("#reportGet").closest("form").submit();

//                 $("#reportButton").prop({"disabled": false, "value": "Сформувати звіт"});
//                 $("#id_model").prop("disabled", false);
//                 $("#id_hyper").prop("disabled", false);
//                 $("#datepicker1").prop("disabled", false);
//                 $("#datepicker2").prop("disabled", false);
//                 $("#reportForm")[0].reset();

//             } else if (taskStatus === "PENDING") {
//                 setTimeout(() => {
//                     console.log('report_id', report_pk);
//                     getTaskStatus(taskID, report_pk)
//                 }, 1000)
//             } else {
//                 return false;
//             }
//         },
//         error: (response) => {
//             console.log(error);
//         }
//     })
// };
