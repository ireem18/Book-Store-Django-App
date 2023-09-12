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
            },
            error: function(data){
                closeModal();
            }
        });
    };

   var saveForm = function (e) {
        e.preventDefault();
        var form = $(this);
        var $popup = $("#modal-book");
        $.ajax({
          url: form.attr("action"),
          data: form.serialize(),
          type: form.attr("method"),
          cache: false,
          dataType: 'json',
          success: function (data) {
            if (data.form_is_valid) {
              $("#book-table tbody").html(data.html_book_list);
              closeModal();
            }
            else {
              $("#modal-book .modal-content").html(data.html_form);
            }
          },
          error: function(data){
            closeModal();
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
    $("#modal-book").on("submit", ".add-book-form", saveForm);
    // Update book
    $("#book-table").on("click", ".edit-book", loadForm);
    $("#modal-book").on("submit", ".edit-book-form", saveForm);
    // Delete book
    $("#book-table").on("click", ".delete-book", loadForm);
});