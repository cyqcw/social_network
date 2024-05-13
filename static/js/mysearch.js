$(document).ready(
    function(){
        // 点击索引按钮，发请求
        $("#submit2index").on("click", function () {
            console.log("索引");
            $.ajax({
                type: "post",
                url: "/buildindex",
                data: {"id": $("#submit2index").attr("id")},
                dataType: "json",
                beforeSend: function() {
                    console.log("索引");
                    // 设置disabled阻止用户继续点击
                    $("#submit2index").attr("disabled", "disabled");
                },
                complete: function () {
                    // 请求完成移除 disabled 属性
                    $("#submit2index").removeAttr("disabled");
                },
                success: function(result){
                    if(result.status == 200){
                        console.log(result.text);
                    }else{
                        alert("索引失败");
                    }
                },
                error: function (jqXHR, textStatus, e) {
                    alert("提交异常："+e);
                }
            });
        })
        // 点击检索按钮，发请求
        $("#btn-submit2search").on("click", function () {
            var keyword = $.trim($('input[name="submit2search"]').val());
            if (keyword == "")
                return;
            $.ajax({
                type: "get",
                url: "/searchindex",
                data: {
                    "id": $("#submit2search").attr("id"),
                    "keyword": keyword
                },
                dataType: "json",
                beforeSend: function() {
                    // 设置disabled阻止用户继续点击
                    $("#btn-submit2search").attr("disabled", "disabled");
                },
                complete: function () {
                    // 请求完成移除 disabled 属性
                    $("#btn-submit2search").removeAttr("disabled");
                },
                success: function(result){
                    if(result.status == 200){
                        console.log("old get")
                        var movie_list = result.text;
                        var movie_oldlist = $("tr.movie-entry");
                        if (movie_oldlist && movie_oldlist.length>0) {
                            // 清空原有表格
                            $("tr.movie-entry").remove();
                            $("ul.pagination").remove();
                        }
                        // 创建搜索结果的表格并插入到前端页面
                        for (var i = 0; i < movie_list.length; i++) {
                            var search_html = '<tr class="movie-entry">'
                            + '<td>' + movie_list[i].id + '</td>'
                            + '<td>' + movie_list[i].movie_title + '</td>'
                            + '<td>' + movie_list[i].movie_directors + '</td>'
                            + '<td>' + movie_list[i].movie_actors + '</td>'
                            + '<td>' + movie_list[i].movie_description + '</td>'
                            + '</tr>';
                            $("table#moview-result-list-table").append($(search_html))
                        }
                        console.log("检索成功");
                    }else if(result.status == 201){
                        alert("检索不到任何结果!");
                    }
                    else{
                        alert("检索失败");
                    }
                },
                error: function (jqXHR, textStatus, e) {
                    alert("提交异常："+e);
                }
            });
        })

        // 点击微博索引按钮，发请求
        $("#weibosubmit2index").on("click", function () {
            $.ajax({
                type: "post",
                url: "/wbbuildindex",
                data: {"id": $("#weibosubmit2index").attr("id")},
                dataType: "json",
                beforeSend: function() {
                    // 设置disabled阻止用户继续点击
                    $("#weibosubmit2index").attr("disabled", "disabled");
                },
                complete: function () {
                    // 请求完成移除 disabled 属性
                    $("#weibosubmit2index").removeAttr("disabled");
                },
                success: function(result){
                    if(result.status == 200){
                        console.log(result.text);
                    }else{
                        alert("索引失败");
                    }
                },
                error: function (jqXHR, textStatus, e) {
                    alert("提交异常："+e);
                }
            });
        })

        // 点击微博检索按钮，发请求
        $("#btn-weibosubmit2search").on("click", function () {
            const keyword = $.trim($('input[name="weibosubmit2search"]').val());
            if (keyword == "")
                return;
            $.ajax({
                type: "get",
                url: "/wbsearchindex",
                data: {
                    "id": $("#weibosubmit2search").attr("id"),
                    "keyword": keyword
                },
                dataType: "json",
                beforeSend: function() {
                    // 设置disabled阻止用户继续点击
                    $("#btn-weibosubmit2search").attr("disabled", "disabled");
                },
                complete: function () {
                    // 请求完成移除 disabled 属性
                    $("#btn-weibosubmit2search").removeAttr("disabled");
                },

                success: function(result){
                    console.log("new get");
                    if(result.status == 200){
                        var note_list = result.text;
                        console.log("note_list", note_list)
                        var note_oldlist = $("tr.note-entry");
                        console.log("note_oldlist", note_oldlist)
                        if (note_oldlist && note_oldlist.length>0) {
                            // 清空原有表格
                            $("tr.note-entry").remove();
                            $("ul.pagination").remove();
                        }
                        // 创建搜索结果的表格并插入到前端页面
                        for (var i = 0; i < note_list.length; i++) {
                            var search_html = '<tr class="note-entry">'
                            + '<td>' + note_list[i].id + '</td>'
                            + '<td>' + note_list[i].content + '</td>'
                            + '<td>' + note_list[i].create_date_time + '</td>'
                            + '<td>' + note_list[i].nickname + '</td>'
                            + '<td>' + note_list[i].ip_location + '</td>'
                            + '<td>' + note_list[i].gender + '</td>'
                            + '</tr>';
                            $("table#note-result-list-table").append($(search_html))
                        }
                        console.log("检索成功");
                    }else if(result.status == 201){
                        alert("检索不到任何结果!");
                    }
                    else{
                        alert("检索失败");
                    }
                },
                error: function (jqXHR, textStatus, e) {
                    alert("提交异常："+e);
                }
            });
        })

        $("input.btn-pos").on("click", function () {
            // 保存按钮的引用
            var $button = $(this);
            // 发送AJAX请求
            $.ajax({
                type: "GET",
                url: "/posannotation",
                data: {
                    "id": $button.attr("id") // 使用保存的引用
                },
                dataType: "json",
                beforeSend: function() {
                    // 禁用按钮
                    $button.attr("disabled", "disabled");
                },
                complete: function () {
                    // 请求完成后启用按钮
                    $button.removeAttr("disabled");
                },
                success: function(result){
                    if(result.status == 200){
                        var note = result.data;
                        var replace_html = '<tr class="note-entry" id=' + note.id + '>'
                            + '<td>' + note.id + '</td>'
                            + '<td>' + note.content + '</td>'
                            + '<td>' + note.create_date_time + '</td>'
                            + '<td>' + note.nickname + '</td>'
                            + '<td>' + note.ip_location + '</td>'
                            + '<td>' + note.gender + '</td>'
                            + '<td>'
                                + '<input type="button" class="form-control btn btn-success btn-pos" value="词性标注" id="{{ data.id }}">'
                                + '<input type="button" class="form-control btn btn-success btn-ner" value="命名实体识别" id="{{ data.id }}">'
                            + '</td>'
                            + '</tr>';
                        $("tr.note-entry#"+note.id).replaceWith(replace_html);
                    }
                    else {
                        alert("词性标注失败");
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    alert("词性标注提交异常：" + errorThrown);
                }
            });
        });

        $("input.btn-ner").on("click", function () {
            // 保存按钮的引用
            var $button = $(this);
            // 发送AJAX请求
            $.ajax({
                type: "GET",
                url: "/nerannotation",
                data: {
                    "id": $button.attr("id") // 使用保存的引用
                },
                dataType: "json",
                beforeSend: function() {
                    // 禁用按钮
                    $button.attr("disabled", "disabled");
                },
                complete: function () {
                    // 请求完成后启用按钮
                    $button.removeAttr("disabled");
                },
                success: function(result) {
                    if (result.status == 200) {
                        var note = result.data;
                        var replace_html = '<tr class="note-entry" id=' + note.id + '>'
                            + '<td>' + note.id + '</td>'
                            + '<td>' + note.content + '</td>'
                            + '<td>' + note.create_date_time + '</td>'
                            + '<td>' + note.nickname + '</td>'
                            + '<td>' + note.ip_location + '</td>'
                            + '<td>' + note.gender + '</td>'
                            + '<td>'
                                + '<input type="button" class="form-control btn btn-success btn-pos" value="词性标注" id="{{ data.id }}">'
                                + '<input type="button" class="form-control btn btn-success btn-ner" value="命名实体识别" id="{{ data.id }}">'
                            + '</td>'
                            + '</td>'
                            + '</tr>';
                        $("tr.note-entry#" + note.id).replaceWith(replace_html);
                    } else {
                        alert("命名实体识别失败");
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    alert("命名实体提交异常：" + errorThrown);
                }
            })
        });

        // 点击检索按钮，发请求chatbotsendbtn
        $("#chatbotsendbtn").on("click", function () {
            var searchtext = $.trim($('#chattextarea').val());
            if (searchtext === "") {
                alert("请输入您的问题");
                return;
            }
            console.log("searchtext ：", searchtext);
            // 将问题添加到聊天窗口的末尾
            var question_html = `
                <div class="item item-right">
                    <div class="bubble bubble-right">${searchtext}</div>
                    <div class="avatar avatar-user"></div>
                </div>
            `;
            $('.content').append(question_html);

            // 清空问题文本框
            $('#chattextarea').val('').focus();

            // 滚动条置底
            var height = $('.content').scrollTop();
            $(".content").scrollTop(height);

            $.ajax({
                type: "get",
                url: "/searchanswer",
                data: {
                    "id": $("#chatbotsendbtn").attr("id"),
                    "text": searchtext
                },
                dataType: "json",
                beforeSend: function() {
                    // 设置 disabled 阻止用户继续点击
                    $("#chatbotsendbtn").attr("disabled", "disabled");
                },
                complete: function () {
                    // 请求完成移除 disabled 属性
                    $("#chatbotsendbtn").removeAttr("disabled");
                },
                success: function(result) {
                    if (result.status === 200) {
                        // 将答案添加到聊天窗口的末尾
                        var answer_html = `
                            <div class="item item-left">
                                <div class="avatar avatar-bot"></div>
                                <div class="bubble bubble-left">${result.answer[0]}</div>
                            </div>
                        `;
                        $('.content').append(answer_html);

                        var answer_html = `
                            <div class="item item-left">
                                <div class="avatar avatar-bot"></div>
                                <div class="bubble bubble-left">${result.answer[1]}</div>
                            </div>
                        `;
                        $('.content').append(answer_html);
                        // 滚动条置底
                        $(".content").scrollTop($('.content').scrollTop());
                        console.log("检索答案成功");
                    } else {
                        // 将答案添加到聊天窗口的末尾
                        var answer_html = `
                            <div class="item item-left">
                                <div class="avatar avatar-bot"></div>
                                <div class="bubble bubble-left">对不起！我不明白您的问题，可以换种问法吗？</div>
                            </div>
                        `;
                        $('.content').append(answer_html);

                        // 滚动条置底
                        $(".content").scrollTop($('.content').scrollTop());
                        console.log("检索不到答案");
                    }
                },
                error: function(jqXHR, textStatus, e) {
                    alert("提交异常：" + e);
                }
            });
        });
})