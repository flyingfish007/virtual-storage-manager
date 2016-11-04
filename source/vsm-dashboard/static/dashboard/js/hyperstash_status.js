
require.config({
    paths:{
        echarts:"../../../../../static/lib/echarts"
    }
});

var refreshInterval=5000;
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
        cCacheAction = ec.init(document.getElementById('divCacheActionRect'));
    	//load
        loadCacheRatio(rbd_id);
        loadCacheAction(rbd_id);
        setInterval(function(){
            loadCacheRatio(rbd_id);
            loadCacheAction(rbd_id);
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
                cCacheRatios.setOption(GetCacheRatio(data.cache_free_size,data.cache_used_size,data.cache_clean_size,data.cache_dirty_size))
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if(XMLHttpRequest.status == 401)
                window.location.href = "/dashboard/auth/logout/";
        }
     });
}

function loadCacheAction(rbd_id){
    $.ajax({
        type: "get",
        url: "/dashboard/vsm/hyperstash_status/"+rbd_id+"/cache_action",
        data: null,
        dataType:"json",
        success: function(data){
                cCacheAction.setOption(
                    GetCacheAction(data)
                )
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
            data:['Dirty','Clean','Used','Free']
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

function GetCacheAction(data){
    option = {
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['Cache Promote','Cache Flush','Cache Evict']
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : data.date
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [
            {
                name:'Cache Promote',
                type:'line',
                tiled: 'total',
                data:data.cache_promote
            },
            {
                name:'Cache Flush',
                type:'line',
                tiled: 'total',
                data:data.cache_flush
            },
            {
                name:'Cache Evict',
                type:'line',
                tiled: 'total',
                data:data.cache_evict
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
                'description': $("#txtDescription").val()
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

function updateHsRbdCacheConfig(){
	var id = $("#id_id").val();
    var cache_dir = $("#id_cache_dir").val();
    var clean_start = $("#id_clean_start").val();
    var enable_memory_usage_tracker = $("#id_enable_memory_usage_tracker").val();
    var object_size = $("#id_object_size").val();
	var cache_total_size = $("#id_cache_total_size").val();
	var cache_dirty_ratio_min = $("#id_cache_dirty_ratio_min").val();
    var cache_dirty_ratio_max = $("#id_cache_dirty_ratio_max").val();
    var cache_ratio_health = $("#id_cache_ratio_health").val();
    var cache_ratio_max = $("#id_cache_ratio_max").val();
    var cache_flush_interval = $("#id_cache_flush_interval").val();
    var cache_evict_interval = $("#id_cache_evict_interval").val();
    var cache_flush_queue_depth = $("#id_cache_flush_queue_depth").val();
    var agent_threads_num = $("#id_agent_threads_num").val();
    var cache_service_threads_num = $("#id_cache_service_threads_num").val();
    var hs_instance_id = $("#id_hs_instance_id").val();

	var data = {
        "id":id,
        "cache_dir":cache_dir,
		"clean_start":clean_start,
        "enable_memory_usage_tracker":enable_memory_usage_tracker,
		"object_size":object_size,
        "cache_total_size":cache_total_size,
		"cache_dirty_ratio_min":cache_dirty_ratio_min,
        "cache_dirty_ratio_max":cache_dirty_ratio_max,
        "cache_ratio_health":cache_ratio_health,
        "cache_ratio_max":cache_ratio_max,
        "cache_flush_interval":cache_flush_interval,
        "cache_evict_interval":cache_evict_interval,
        "cache_flush_queue_depth":cache_flush_queue_depth,
        "agent_threads_num":agent_threads_num,
        "cache_service_threads_num":cache_service_threads_num,
        "hs_instance_id":hs_instance_id
    };
	var postData = JSON.stringify(data);
	token = $("input[name=csrfmiddlewaretoken]").val();

	$.ajax({
		type: "post",
		url: "/dashboard/vsm/hyperstash_status/update_action/",
		data: postData,
		dataType:"json",
		success: function(data){
				console.log(data);
				window.location.href="/dashboard/vsm/hyperstash_status/"+hs_instance_id+"/list_rbd";
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
