
require.config({
    paths:{
        echarts:"../../static/lib/echarts",
    }
});

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

    }
);


$(document).ready(function(){
    //Hide Page Title
    HidePageHeader();

    loadVersion();
});


function HidePageHeader(){
    $(".page-header").hide();
}


function loadVersion(){
    $.ajax({
	type: "get",
	url: "/dashboard/vsm/version/",
	data: null,
	dataType:"json",
	success: function(data){
         //console.log(data);
        $("#lblVersionUpdate")[0].innerHTML =data.update;

        if(data.version == null)
            $("#lblVersion")[0].innerHTML= "--";
        else
            $("#lblVersion")[0].innerHTML= data.version;

	    if(data.ceph_version == null)
            $("#lblCephVersion")[0].innerHTML= "--";
        else
            $("#lblCephVersion")[0].innerHTML= data.ceph_version;
	   },
    error: function (XMLHttpRequest, textStatus, errorThrown) {
            if(XMLHttpRequest.status == 401)
                window.location.href = "/dashboard/auth/logout/";
        }
    });
}
