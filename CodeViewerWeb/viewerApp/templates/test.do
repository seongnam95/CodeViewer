<script>
    function anyncMovePage(url){
        var ajaxOption = {
            url : url,
            async : true,
            type : "POST",
            dataType : "html",
            cashe : false
        };

        $.ajax(ajaxOption).done(function(data) {
            $('#bodyContents').children().remove();
            $('#bodyContents').html(data);
        });
    }
</script>