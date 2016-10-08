
require.config({
    paths:{
        echarts:"../../../../../static/lib/echarts"
    }
});

var refreshInterval=15000;
var token = $("input[name=csrfmiddlewaretoken]").val();
require(
    [
        'echarts',
        'echarts/chart/line',
        'echarts/chart/bar',
        'echarts/chart/pie',
        'echarts/chart/gauge'
    ],
    function(ec){
        cCacheRatios = ec.init(document.getElementById('divCacheRatioRect'));
        rbd_id = document.getElementById('divCacheRatioRect').title;
    	//load Capacity
        loadCacheRatio(rbd_id);
        setInterval(function(){
            loadCacheRatio(rbd_id);
        },refreshInterval);
    }
);

function loadCacheRatio(rbd_id){
    $.ajax({
        type: "get",
        url: "/dashboard/vsm/hyperstash_status/"+rbd_id+"/cache_ratio",
        data: null,
        dataType:"json",
        success: function(data){
                cCacheRatios.setOption(GetCacheRatio(data.free,data.used,data.clean,data.dirty))
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if(XMLHttpRequest.status == 401)
                window.location.href = "/dashboard/auth/logout/";
        }
     });
}

function GetCacheRatio(FREE,USED,CLEAN,DIRTY){
    option = {
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data:['Free','Used','Clean','Dirty']
        },
        series: [
            {
                name:'source',
                type:'pie',
                selectedMode: 'single',
                radius: [0, '30%'],

                label: {
                    normal: {
                        position: 'inner'
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data:[
                    {value:FREE, name:'Free', selected:true},
                    {value:USED, name:'Used'}
                ]
            },
            {
                name:'source',
                type:'pie',
                radius: ['40%', '55%'],

                data:[
                    {value:FREE, name:'Free'},
                    {value:CLEAN, name:'Clean'},
                    {value:DIRTY, name:'Dirty'}
                ]
            }
        ]
    };
    return option;
}

function addHsInstance(){
	//Check the field is should not null
	if($("#txtHsInstanceName").val() == ""){
		showTip("error","The field is marked as '*' should not be empty");
		return  false;
	}
    if($("#txtIpAddress").val() == ""){
		showTip("error","The field is marked as '*' should not be empty");
		return  false;
	}
	var data = {
			"hs_instance":{
				"hs_instance_name":$("#txtHsInstanceName").val(),
				'ip_address': $("#txtIpAddress").val(),
                'description': $("#description").val()
			}
	};
	var postData = JSON.stringify(data);
	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/hyperstash_status/create_hs_instance/",
		data: postData,
		dataType:"json",
		success: function(data){
				//console.log(data);
                if(data.status == "OK"){
                    window.location.href="/dashboard/vsm/hyperstash_status/";
                }
                else{
                    showTip("error",data.message);
                }
		   	},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
				if(XMLHttpRequest.status == 500)
                	showTip("error","INTERNAL SERVER ERROR")
			},
		headers: {
			"X-CSRFToken": token
			},
		complete: function(){

		}
    });
}
