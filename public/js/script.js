function getBuildLog(bid) {
    $.get('/push/build/'+ bid, function(data) {
        $("pre.build" + bid).html(data);
        console.log(data);
        getBuildLog(bid);
    });
}

$(function(){
    $("#start-new-build").unbind().bind('click', function(){
        var $button = $(this);
        var data = {};
        data['name'] = $("#name").val();
        data['command'] = $("#command").val();
        $.post('/ajax/build/new', data, function(response){
            getBuildLog(response.build)
        });
        return false;
    });
});