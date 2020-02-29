(function ($) {

    $(document).ready(function () {
        // file org_file_name
        $('.field-org_file_name input[type=text]').attr('readonly', 'readonly').css('background', '#8080801c');
        $(document).on('change', '.field-file input[type=file]', function () {
            // 원본파일명 저장
            var org_file_name = $(this).val().split('\\');
            org_file_name = org_file_name[org_file_name.length - 1];
            if ($.trim(org_file_name) !== '') {
                $(this).parents('.field-file').next().find('input[type=text]').val(org_file_name);
            }
        });
    });


})(django.jQuery);