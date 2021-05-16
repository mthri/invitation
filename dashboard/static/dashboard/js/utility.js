$(() => {
    $('.mobile-check').on('change keyup paste', (e) => {
        let input = $(e.target)
        let mobileRegex = new RegExp('09(1[0-9]|3[1-9]|2[0-9])-?[0-9]{3}-?[0-9]{4}')
        if (!mobileRegex.test(input.val())) {
            input.removeClass('is-valid')
            input.addClass('is-invalid')
        }
        else {
            input.removeClass('is-invalid')
            input.addClass('is-valid')

        }
    })

    $('.ajax-submit').submit((e)=>{
        e.preventDefault()
        let form = $(e.target)
        // form.find(':input').prop("disabled", true);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            method: form.attr('method')
        }).done((data)=>{
            swal({
                title: "",
                text: "عملیات با موفقیت انجام شد",
                type: "success",
                showCancelButton: false,
                confirmButtonText: "ادامه",
                closeOnConfirm: true,
            })
            // form.find(':input').prop("disabled", false);
            form.trigger("reset")
        }).fail((errors)=>{
            swal({
                title: "",
                text: "عملیات با خطا مواجه شده است",
                type: "error",
                showCancelButton: false,
                confirmButtonText: "ادامه",
                closeOnConfirm: true,
            })
            // form.find(':input').prop("disabled", false);
            clearError(form)
            showError(errors.responseJSON)
        })
    })
})

function showError(errors) {
    Object.entries(errors).forEach(([inputName, messageArray]) => {
        Object.entries(messageArray).forEach(([_, message]) => {
            let input = $(`[name=${inputName}]`)
            input.removeClass('is-valid')
            input.addClass('is-invalid')
            input.parent().append(`<div class="form-control-feedback text-danger">${message.message}</div>`)
        })
    }); 
}

function clearError(form){
    form.find('.form-control-feedback').remove()
    $(form).find('.is-invalid').removeClass('is-invalid')
}