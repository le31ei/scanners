layui.use(['form', 'layer'], function () {
    var form = layui.form,
        layer = layui.layer,
        $ = layui.jquery;

    form.on('submit(add)', function (data) {
        $.post('', data.field, function (msg) {
            if (msg.code === "1"){
                layer.msg(msg.msg, function () {
                    this.reset();
                });
            }else {
                layer.alert(msg.msg);
                }
        });
        return false;
    });
});