$("#id_type").on("click", () => {

    if ($("#id_type").val() === "Integer") {
        $("#hide3").attr({ "class": "col" });
        $("#hide4").attr({ "class": "col" });
    } else {
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

        let notShow = "" ? (response.type === "Integer") : "not-show";

        $("#columnRows").append(
            `<form class="columnRow" action="/new_column/delete/${response.id}/" method="GET">
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
        type: "GET",
        url: `${this.action}`
    })
    .done((response) => {
        $(this).remove();
    })
    .fail((err) => {
        return false;
    })
});
