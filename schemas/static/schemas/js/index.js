$("#id_type").on("click", () => {

    if ($("#id_type").val() === "Integer") {
        $("#hide3").attr({ "class": "col" });
        $("#hide4").attr({ "class": "col" });
    } else {
        $("#hide3").attr({ "class": "col d-none" });
        $("#hide4").attr({ "class": "col d-none" });
    }
})

$("#createColumn").submit(function (e) {
    const formData = $(this).serialize();

    e.preventDefault();

    $.ajax({
        type: "POST",
        url: "{% url 'schemas:create_column' %}",
        data: formData,
        success: (response) => {
            $("#createColumn").trigger('reset');

            if (response.type === "Integer") {
                notShow = "";
            } else {
                notShow = "not-show"
            };

            $("#columnRows").append(
                `<form action="new_column/delete/${response.id}" method="get">
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
                        <div class="col">
                            <label class="form-label">Order</label>
                            <input type="text" class="form-control" readonly placeholder="${response.order}">
                        </div>
                        <div class="col">
                            <button type="submit" class="btn btn-danger col-submit">Delete</button>
                        </div>
                    </div>
                </form>`
            );
        },
        error: (response) => {
            return false;
        }
    })
});