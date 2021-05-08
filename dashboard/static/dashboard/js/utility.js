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
})