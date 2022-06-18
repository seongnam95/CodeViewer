function excel_upload(){
    if (confirm('엑셀을 반영 하시겠습니까?')){

       // Get form
       var form = $('#frm_excel')[0];

       // Create an FormData object
       var formData = new FormData(form);

       var params = "";
       var msg = "";
       alert($('#frm_excel')[0]);
       $.ajax({
           url: "upload/",
           type: "POST",
           enctype: 'multipart/form-data',
           processData: false,
           contentType: false,
           data: formData,
           dataType: "JSON", // JSON 리턴
           success:function(data){
             $('#address_table').html(data)
           },
           error: function(request, status, error){
             alert('서버와의 연결에 실패하였습니다.');
           }
       });
    }
}