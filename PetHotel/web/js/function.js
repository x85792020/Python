//----- OREDER 客製化處理------------------
//取得所有資料
function getAllOrderData(petName="",mode=""){
    //有eel開頭的 都是python function
    //遊戲規則 第一個() 丟給python的參數 第二個()python跑完之後 回傳的資料給哪個function
    eel.getOrderDataPy(petName,mode)(outputOrderData);
}
// 輸出成table
function outputOrderData(rawdata){
    var htmlTemplate = '<table class="table customer-table table-hover">';
    htmlTemplate+='<tr class="header-style">';
    htmlTemplate+='<th>訂單編號</th>';
    htmlTemplate+='<th>寵物名稱</th>';
    htmlTemplate+='<th>日期</th>';
    htmlTemplate+='<th>房間編號</th>';
    htmlTemplate+='<th>負責員工</th>';
    htmlTemplate+='<th>功能</th>';
    htmlTemplate+='</tr>';
    var list = jQuery.parseJSON(rawdata)
    for(var i =0;i<list.length;i++){
        htmlTemplate = htmlTemplate + '<tr>';
        htmlTemplate = htmlTemplate + '<td>'+list[i].order_id + '</td>';
        htmlTemplate = htmlTemplate + '<td>'+list[i].pet_name + '</td>';
        htmlTemplate = htmlTemplate + '<td>'+list[i].date + '</td>';
        htmlTemplate = htmlTemplate + '<td>'+list[i].room_name + '</td>';
        htmlTemplate = htmlTemplate + '<td>'+list[i].empoloyee_name + '</td>';
        htmlTemplate = htmlTemplate + '<td>';
        htmlTemplate = htmlTemplate + '<button type="button" class="btn btn-primary edit-btn" target-id="'+list[i].order_id+'">編輯</button>';
        htmlTemplate = htmlTemplate + '<button type="button" class="btn btn-primary del-btn" target-id="'+list[i].order_id+'">刪除</button>';
        htmlTemplate = htmlTemplate + '</td>';
        htmlTemplate = htmlTemplate + '</tr>';
    }
    htmlTemplate += '</table>';
    //傳給tabel
    $('#order-info').empty();
    $('#order-info').append(htmlTemplate);
}
//取得從table取得的select 下拉式選單
function getPetOption(){
    eel.getPetOptionPy()(createPetOption);
}
//產生 寵物下拉式選單
function createPetOption(rawdata){
    var htmlTemplate = "<option>請選擇</option>";
    var list = jQuery.parseJSON(rawdata)
    for(var i =0;i<list.length;i++){
        htmlTemplate = htmlTemplate + '<option value="'+list[i].value+'">'+list[i].text+'</option>';
    }
    //生成選項給寵物名稱
    $('#pet_id').empty();
    $('#pet_id').append(htmlTemplate)
}

//連接Python 取得 employee資料
function getEmployeeOption(){
    eel.getEmployeeOptionPy()(createEmployeeOption);
}
//取得員工下拉式選單
function createEmployeeOption(rawdata){
    var htmlTemplate = "<option>請選擇</option>";
    var list = jQuery.parseJSON(rawdata)
    for(var i =0;i<list.length;i++){
        htmlTemplate = htmlTemplate + '<option value="'+list[i].value+'">'+list[i].text+'</option>';
    }
    //生成選項給寵物名稱
    $('#employee_id').empty();
    $('#employee_id').append(htmlTemplate)
}
//連接Python 取得rooms資料
function getRoomOption(){
    var data;   
    data = eel.getRoomOptionPy()(createRoomOption);
}
//建立房間選項 select
function createRoomOption(rawdata){
    var htmlTemplate = "<option>請選擇</option>";
    var list = jQuery.parseJSON(rawdata)
    for(var i =0;i<list.length;i++){
        htmlTemplate = htmlTemplate + '<option value="'+list[i].value+'">'+list[i].text+'</option>';
    }
    //生成選項給寵物名稱
    $('#room_id').empty();
    $('#room_id').append(htmlTemplate)
}

//ORDER 刪除
function delOrder(order_id){
    //執行python 刪除function
    eel.delOrderPy(order_id)(delOrderMsg);
}
function delOrderMsg(msg){
    $('#msg').modal('show');
    //執行python 刪除function
    if(msg == 'success'){
        alert('刪除完成!');
        getAllOrderData();

    }else{
        alert('刪除失敗,請重新整理再進行操作!');
    }

}

function submitOrderData(orderData){
    var addOrEdit = "";
    addOrEdit = orderData.order_id == ""?"Add":"Edit";
    eel.submitOrderDataPy(addOrEdit,orderData)(submitMsg);
}
function submitMsg(output){
    alert(output);
    getAllOrderData();
    //初始化form 表單
    //新增模式初始化
    //createModelInit();
}

//取得單一ORDER 資料
function getOrderData(order_id){
    eel.getOrderFormDataPy(order_id)(showOrder);
}
function showOrder (outputData){
    var obj = jQuery.parseJSON(outputData)
    if(obj.successCode ==""){
        var orderData = obj.data[0];
        //訂單編號
        $('#order_id').val(orderData.order_id);
        $('#pet_id').val(orderData.pet_id);
        $('#room_id').val(orderData.room_id);
        $('#employee_id').val(orderData.employee_id);
        $('#date').val(orderData.date);
        $('#price').val(orderData.price);
    }else{
        alert(outputData.successCode);
    }
    
}
//取得各操作 範例
function runSQL(sql){
    eel.runSQLPy(sql)(showMsg);
}
function showMsg(output){
    var obj = jQuery.parseJSON(output);
    if(obj.successCode =="fail"){
        $('#output-block').empty();
        $('#output-block').append(obj.msg);
    }else{
        if(obj.isTable){
            var cols = obj.columns;
            var data = obj.data
            var rawData = obj.data;
            var htmlTemplate = "";
            //畫TABLE
            var htmlTemplate = '<table class="table table-hover">';
            //先畫欄位名稱
            htmlTemplate = htmlTemplate + '<tr>';
            for(var i =0;i<cols.length;i++){
                htmlTemplate = htmlTemplate + '<th>'+cols[i]+'</th>';
            }
            //產生資料
            for(var i =0;i<data.length;i++){
                
                //每一行先產生個ROW 給他
                htmlTemplate = htmlTemplate + '<tr>';
                //這一行資料總共有這些值
                var valueArray = data[i];
                for(var index = 0;index< valueArray.length;index++){
                    htmlTemplate = htmlTemplate + '<td>'+valueArray[index]+'</td>';
                }
                htmlTemplate = htmlTemplate + '</tr>';
            }
            htmlTemplate = htmlTemplate + '</tr>';
            htmlTemplate += '</table>';
            $('#output-block').empty();
            $('#output-block').append(htmlTemplate);
        }else{
            //新增、編輯、刪除
            $('#output-block').empty();
            $('#output-block').text(obj.msg);
        }
        
    }
}
//計算前五名
function getOraderMonthRank(year,month,day){
    eel.getOraderMonthRankPy(year,month,day)(createRankBlock);

}
function createRankBlock(output){
    var obj = jQuery.parseJSON(output);
    var htmlTemplate = '';
    for(var i = 0;i<obj.length;i++){
        htmlTemplate += '<div class="rank-item">(員工編號:'+obj[i].employee_id+')'+obj[i].emplyee_name+'<span class="rank-count">負責數量:'+obj[i].order_count+'張</span></div>';
    }
    $('#rank-block').empty();
    $('#rank-block').append(htmlTemplate);
}

//--------------通用區域------------------------------------
//通用型TABLE Function
function getTableInfo(tableName,target){
    eel.getTableInfoPy(tableName,target)(createTableHtml);
}
//通用型 TABLE  HTML產生　函數
function createTableHtml(output){
    var obj = jQuery.parseJSON(output);
    var cols = obj.columns;
    var data = obj.data;
    var target = obj.target;
    //畫TABLE
    var htmlTemplate = '<table class="table customer-table table-hover">';
    //先畫欄位名稱
    htmlTemplate = htmlTemplate + '<tr class="header-style">';
    for(var i =0;i<cols.length;i++){
        htmlTemplate = htmlTemplate + '<th>'+cols[i]+'</th>';
    }
    //產生資料
    for(var i =0;i<data.length;i++){
        
        //每一行先產生個ROW 給他
        htmlTemplate = htmlTemplate + '<tr>';
        //這一行資料總共有這些值
        var valueArray = data[i];
        for(var index = 0;index< valueArray.length;index++){
            htmlTemplate = htmlTemplate + '<td>'+valueArray[index]+'</td>';
        }
        htmlTemplate = htmlTemplate + '</tr>';
    }
    htmlTemplate = htmlTemplate + '</tr>';
    htmlTemplate += '</table>';
    $(target).empty();
    $(target).append(htmlTemplate);
}
function getCalculate(selectOption){
    eel.getCalculatePy(selectOption)(createDetailInfo);
}

function createDetailInfo(output){
    $('#detail-search').empty();
    var obj = jQuery.parseJSON(output);
    var option = obj.columns[0];
    var data = obj.data[0][0];
    var htmlTemplate = '';
    
    if(option == 'COUNT'){
        htmlTemplate += '<div class="rank-item">('+option+')目前訂單總數:'+data+'筆</div>';
    }
    else if(option == 'SUM'){
        htmlTemplate += '<div class="rank-item">('+option+')目前訂單總入住金額:'+data+'元</div>';
    }
    else if(option == 'AVG'){
        htmlTemplate += '<div class="rank-item">('+option+')平均訂單入住金額:'+data+'元</div>';
    }
    else if(option == 'MAX'){
        htmlTemplate += '<div class="rank-item">('+option+')訂單最高入住金額:'+data+'元</div>';
    }
    else if(option == 'MIN'){
        htmlTemplate += '<div class="rank-item">('+option+')訂單最低入住金額:'+data+'元</div>';
    }
    $('#detail-search').append(htmlTemplate);
    debugger;
}