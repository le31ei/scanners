layui.use(['table'], function () {
    var table = layui.table,
        $ = layui.jquery;
    table.init('listtable', {
        limit: 10
    });

    table.on('tool(listtable)', function (obj) {
        var data = obj.data;
        if (obj.event === 'detail'){
            //跳转到新的页面
            window.location.href = '/detail_scan/'+data.uuid;
        }else if (obj.event === 'download') {
            //下载
            window.location.href = '/export/'+data.uuid;
        }else if (obj.event === 'del') {
            //删除
            alert('del');
        }

    })
});