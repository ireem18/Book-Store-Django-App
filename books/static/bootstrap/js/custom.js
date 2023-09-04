$(function () {
    var loadForm = function () {
        var btn = $(this);
        var $popup = $("#modal-book");
        $.ajax({
            url: btn.attr("data-form-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $popup.modal("show");
            },
            success: function (data) {
                $("#modal-book .modal-content").html(data.html_form);
          }
        });
    };

    var closeModal = function () {
       location.reload();
    };

    // Close book
    $(".close-modal").click(closeModal)
    // Create book
    $(".add-book").click(loadForm);
    // Update book
    $("#book-table").on("click", ".edit-book", loadForm);
    // Delete book
    $("#book-table").on("click", ".delete-book", loadForm);
});